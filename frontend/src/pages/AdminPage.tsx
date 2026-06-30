import { useEffect, useState } from "react";

import {
  changeAdminPassword,
  createFloorAsAdmin,
  getAdminSettings,
  getAdminStatus,
  loginAdmin,
  logoutAdmin,
  setupAdminPassword,
  updateAdminSettings,
  uploadFloorMapAsAdmin
} from "../services/adminService";
import { listFloors } from "../services/surveyService";
import type { AdminSettings } from "../types/admin";
import type { Floor } from "../types/survey";
import "../styles/admin.css";

const ADMIN_TOKEN_KEY = "wavetracker_admin_token";

export function AdminPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [initialized, setInitialized] = useState(false);
  const [token, setToken] = useState<string | null>(null);

  const [setupPassword, setSetupPassword] = useState("");
  const [setupPasswordConfirm, setSetupPasswordConfirm] = useState("");
  const [loginPassword, setLoginPassword] = useState("");

  const [settings, setSettings] = useState<AdminSettings | null>(null);
  const [floors, setFloors] = useState<Floor[]>([]);
  const [newFloorName, setNewFloorName] = useState("Main Floor");
  const [selectedFloorId, setSelectedFloorId] = useState("");
  const [mapFile, setMapFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const [currentPassword, setCurrentPassword] = useState("");
  const [nextPassword, setNextPassword] = useState("");
  const [nextPasswordConfirm, setNextPasswordConfirm] = useState("");
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    const existingToken = window.localStorage.getItem(ADMIN_TOKEN_KEY);
    let active = true;

    getAdminStatus()
      .then((status) => {
        if (!active) {
          return;
        }

        setInitialized(status.initialized);
        setToken(status.initialized && existingToken ? existingToken : null);
        setNotice(null);
      })
      .catch((loadError) => {
        if (active) {
          setError(loadError instanceof Error ? loadError.message : "Failed to load admin status");
        }
      })
      .finally(() => {
        if (active) {
          setLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (token == null) {
      setSettings(null);
      return;
    }

    let active = true;
    Promise.all([getAdminSettings(token), listFloors()])
      .then(([settingsResponse, floorResponse]) => {
        if (!active) {
          return;
        }
        setSettings(settingsResponse.settings);
        setFloors(floorResponse);
        if (floorResponse.length > 0) {
          setSelectedFloorId((current) =>
            current.length > 0 ? current : settingsResponse.settings.default_floor_id ?? floorResponse[0].id
          );
        }
      })
      .catch((loadError) => {
        if (!active) {
          return;
        }
        window.localStorage.removeItem(ADMIN_TOKEN_KEY);
        setToken(null);
        setNotice(null);
        setError(loadError instanceof Error ? loadError.message : "Failed to load admin data");
      });

    return () => {
      active = false;
    };
  }, [token]);

  async function refreshFloors() {
    const nextFloors = await listFloors();
    setFloors(nextFloors);
    if (nextFloors.length > 0 && selectedFloorId.length === 0) {
      setSelectedFloorId(nextFloors[0].id);
    }
  }

  return (
    <section className="admin-shell">
      <header className="admin-head">
        <h2>Management Console</h2>
        <p>Floor map and platform settings are managed from this secured area.</p>
      </header>

      {loading && <p className="admin-muted">Loading admin state...</p>}
      {error && <p className="admin-error">{error}</p>}
      {notice && <p className="admin-notice">{notice}</p>}

      {!loading && !initialized && (
        <section className="admin-card">
          <h3>Initial setup</h3>
          <p className="admin-muted">Set admin password for first access.</p>
          <input
            type="password"
            placeholder="New password"
            value={setupPassword}
            onChange={(event) => setSetupPassword(event.target.value)}
          />
          <input
            type="password"
            placeholder="Confirm password"
            value={setupPasswordConfirm}
            onChange={(event) => setSetupPasswordConfirm(event.target.value)}
          />
          <button
            type="button"
            disabled={busy}
            className="admin-primary"
            onClick={async () => {
              if (setupPassword.length < 8) {
                setError("Password must be at least 8 characters");
                return;
              }
              if (setupPassword !== setupPasswordConfirm) {
                setError("Password confirmation does not match");
                return;
              }

              setBusy(true);
              setError(null);
              setNotice(null);
              try {
                await setupAdminPassword(setupPassword);
                const login = await loginAdmin(setupPassword);
                window.localStorage.setItem(ADMIN_TOKEN_KEY, login.token);
                setInitialized(true);
                setToken(login.token);
                setSetupPassword("");
                setSetupPasswordConfirm("");
                setNotice("Admin password has been set.");
              } catch (setupError) {
                setError(setupError instanceof Error ? setupError.message : "Failed to initialize password");
              } finally {
                setBusy(false);
              }
            }}
          >
            Save admin password
          </button>
        </section>
      )}

      {!loading && initialized && token == null && (
        <section className="admin-card">
          <h3>Admin login</h3>
          <input
            type="password"
            placeholder="Admin password"
            value={loginPassword}
            onChange={(event) => setLoginPassword(event.target.value)}
          />
          <button
            type="button"
            disabled={busy || loginPassword.length === 0}
            className="admin-primary"
            onClick={async () => {
              setBusy(true);
              setError(null);
              setNotice(null);
              try {
                const login = await loginAdmin(loginPassword);
                window.localStorage.setItem(ADMIN_TOKEN_KEY, login.token);
                setToken(login.token);
                setLoginPassword("");
                setNotice("Logged in as administrator.");
              } catch (loginError) {
                setError(loginError instanceof Error ? loginError.message : "Login failed");
              } finally {
                setBusy(false);
              }
            }}
          >
            Login
          </button>
        </section>
      )}

      {!loading && initialized && token != null && settings != null && (
        <div className="admin-grid">
          <section className="admin-card">
            <div className="admin-card-head">
              <h3>Settings</h3>
              <button
                type="button"
                className="admin-secondary"
                disabled={busy}
                onClick={async () => {
                  setBusy(true);
                  setError(null);
                  setNotice(null);
                  try {
                    await logoutAdmin(token);
                    window.localStorage.removeItem(ADMIN_TOKEN_KEY);
                    setToken(null);
                    setSettings(null);
                    setNotice("Logged out.");
                  } catch (logoutError) {
                    setError(logoutError instanceof Error ? logoutError.message : "Logout failed");
                  } finally {
                    setBusy(false);
                  }
                }}
              >
                Logout
              </button>
            </div>
            <label htmlFor="dashboard-title">Dashboard title</label>
            <input
              id="dashboard-title"
              type="text"
              value={settings.dashboard_title}
              onChange={(event) =>
                setSettings((previous) =>
                  previous == null ? previous : { ...previous, dashboard_title: event.target.value }
                )
              }
            />

            <label htmlFor="default-floor">Default floor ID</label>
            <input
              id="default-floor"
              type="text"
              value={settings.default_floor_id ?? ""}
              onChange={(event) =>
                setSettings((previous) =>
                  previous == null
                    ? previous
                    : {
                        ...previous,
                        default_floor_id:
                          event.target.value.trim().length > 0 ? event.target.value.trim() : null
                      }
                )
              }
            />

            <label htmlFor="maintenance-message">Maintenance message</label>
            <input
              id="maintenance-message"
              type="text"
              value={settings.maintenance_message ?? ""}
              onChange={(event) =>
                setSettings((previous) =>
                  previous == null
                    ? previous
                    : {
                        ...previous,
                        maintenance_message:
                          event.target.value.trim().length > 0 ? event.target.value : null
                      }
                )
              }
            />

            <button
              type="button"
              disabled={busy}
              className="admin-primary"
              onClick={async () => {
                setBusy(true);
                setError(null);
                setNotice(null);
                try {
                  const updated = await updateAdminSettings(token, {
                    dashboard_title: settings.dashboard_title,
                    default_floor_id: settings.default_floor_id,
                    maintenance_message: settings.maintenance_message
                  });
                  setSettings(updated.settings);
                  setNotice("Settings updated.");
                } catch (updateError) {
                  setError(updateError instanceof Error ? updateError.message : "Failed to update settings");
                } finally {
                  setBusy(false);
                }
              }}
            >
              Save settings
            </button>
          </section>

          <section className="admin-card">
            <h3>Floor management</h3>
            <div className="admin-inline">
              <input
                type="text"
                value={newFloorName}
                onChange={(event) => setNewFloorName(event.target.value)}
                placeholder="New floor name"
              />
              <button
                type="button"
                disabled={busy || newFloorName.trim().length === 0}
                className="admin-primary"
                onClick={async () => {
                  setBusy(true);
                  setError(null);
                  setNotice(null);
                  try {
                    await createFloorAsAdmin(token, newFloorName.trim());
                    setNewFloorName("");
                    await refreshFloors();
                    setNotice("Floor created.");
                  } catch (createError) {
                    setError(createError instanceof Error ? createError.message : "Failed to create floor");
                  } finally {
                    setBusy(false);
                  }
                }}
              >
                Add floor
              </button>
            </div>

            <select
              value={selectedFloorId}
              onChange={(event) => setSelectedFloorId(event.target.value)}
            >
              <option value="">Select floor</option>
              {floors.map((floor) => (
                <option key={floor.id} value={floor.id}>
                  {floor.name}
                </option>
              ))}
            </select>

            <div className="admin-inline">
              <input
                type="file"
                accept="image/*"
                disabled={busy || selectedFloorId.length === 0}
                onChange={(event) => setMapFile(event.target.files?.[0] ?? null)}
              />
              <button
                type="button"
                disabled={busy || selectedFloorId.length === 0 || mapFile == null}
                className="admin-primary"
                onClick={async () => {
                  if (mapFile == null || selectedFloorId.length === 0) {
                    return;
                  }
                  setBusy(true);
                  setError(null);
                  setNotice(null);
                  try {
                    await uploadFloorMapAsAdmin(token, selectedFloorId, mapFile);
                    setMapFile(null);
                    await refreshFloors();
                    setNotice("Map uploaded.");
                  } catch (uploadError) {
                    setError(uploadError instanceof Error ? uploadError.message : "Failed to upload map");
                  } finally {
                    setBusy(false);
                  }
                }}
              >
                Upload map
              </button>
            </div>
          </section>

          <section className="admin-card">
            <h3>Password</h3>
            <p className="admin-muted">Changing password logs out all active admin sessions.</p>
            <input
              type="password"
              placeholder="Current password"
              value={currentPassword}
              onChange={(event) => setCurrentPassword(event.target.value)}
            />
            <input
              type="password"
              placeholder="New password"
              value={nextPassword}
              onChange={(event) => setNextPassword(event.target.value)}
            />
            <input
              type="password"
              placeholder="Confirm new password"
              value={nextPasswordConfirm}
              onChange={(event) => setNextPasswordConfirm(event.target.value)}
            />
            <button
              type="button"
              className="admin-primary"
              disabled={busy || currentPassword.length === 0 || nextPassword.length < 8}
              onClick={async () => {
                if (nextPassword !== nextPasswordConfirm) {
                  setError("New password confirmation does not match");
                  return;
                }

                setBusy(true);
                setError(null);
                setNotice(null);
                try {
                  await changeAdminPassword(token, currentPassword, nextPassword);
                  window.localStorage.removeItem(ADMIN_TOKEN_KEY);
                  setToken(null);
                  setCurrentPassword("");
                  setNextPassword("");
                  setNextPasswordConfirm("");
                  setNotice("Password changed. Please login again.");
                } catch (changeError) {
                  setError(changeError instanceof Error ? changeError.message : "Failed to change password");
                } finally {
                  setBusy(false);
                }
              }}
            >
              Change password
            </button>
          </section>
        </div>
      )}
    </section>
  );
}