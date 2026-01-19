import { useState } from "react";
import Container from "../components/Container";
import { login } from "../api/auth";
import { setToken } from "../auth/token";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);

  async function onLogin() {
    setMsg("");
    setLoading(true);
    try {
      const r = await login(email, password);
      setToken(r.access_token);
      nav("/");
    } catch (e: any) {
      setMsg(e?.response?.data?.detail ?? "Login error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Container>
      <div className="max-w-lg mx-auto">
        <h1 className="text-2xl font-semibold mb-3">Login</h1>

        <div className="bg-white border rounded-xl p-4 space-y-3">
          <input
            className="w-full border rounded-lg p-2"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="email@uce.edu.ec"
          />
          <input
            className="w-full border rounded-lg p-2"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="password"
          />
          <button
            className="w-full bg-black text-white rounded-lg p-2 disabled:opacity-60"
            onClick={onLogin}
            disabled={loading}
          >
            {loading ? "Signing in..." : "Sign in"}
          </button>

          {msg && <p className="text-sm text-red-700">{msg}</p>}
        </div>
      </div>
    </Container>
  );
}
