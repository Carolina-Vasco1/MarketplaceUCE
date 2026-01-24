import { useState } from "react";
import Container from "../components/Container";
import { requestOtp, verifyOtp, register } from "../api/auth";
import { setToken } from "../auth/token";
import { useNavigate } from "react-router-dom";

export default function RegisterOTP() {
  const nav = useNavigate();
  const [step, setStep] = useState<1 | 2 | 3>(1);

  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<"buyer" | "seller">("buyer");

  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);

  async function onRequestOTP() {
    setMsg("");
    setLoading(true);
    try {
      await requestOtp(email);
      setStep(2);
      setMsg("OTP sent. Check your email.");
    } catch (e: any) {
      setMsg(e?.response?.data?.detail ?? "Error requesting OTP");
    } finally {
      setLoading(false);
    }
  }

  async function onVerifyOTP() {
    setMsg("");
    setLoading(true);
    try {
      await verifyOtp(email, code);
      setStep(3);
      setMsg("Email verified. You can now register.");
    } catch (e: any) {
      setMsg(e?.response?.data?.detail ?? "Invalid OTP");
    } finally {
      setLoading(false);
    }
  }

  async function onRegister() {
    setMsg("");
    setLoading(true);
    try {
      const r = await register(email, password, role);
      setToken(r.access_token);
      nav("/");
    } catch (e: any) {
      setMsg(e?.response?.data?.detail ?? "Registration error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Container>
      <div className="max-w-lg mx-auto">
        <h1 className="text-2xl font-semibold mb-3">
          Register with OTP
        </h1>

        <div className="bg-white border rounded-xl p-4 space-y-3">
          {step === 1 && (
            <>
              <label className="text-sm font-medium">Email</label>
              <input
                className="w-full border rounded-lg p-2"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@gmail.com"
              />
              <button
                className="w-full bg-black text-white rounded-lg p-2 disabled:opacity-60"
                onClick={onRequestOTP}
                disabled={loading}
              >
                {loading ? "Sending..." : "Send OTP"}
              </button>
            </>
          )}

          {step === 2 && (
            <>
              <div className="text-sm text-gray-600">
                Email: <b>{email}</b>
              </div>

              <label className="text-sm font-medium">OTP code</label>
              <input
                className="w-full border rounded-lg p-2"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="6 digits"
              />
              <button
                className="w-full bg-black text-white rounded-lg p-2 disabled:opacity-60"
                onClick={onVerifyOTP}
                disabled={loading}
              >
                {loading ? "Verifying..." : "Verify OTP"}
              </button>
            </>
          )}

          {step === 3 && (
            <>
              <div className="text-sm text-gray-600">
                Verified email: <b>{email}</b>
              </div>

              <label className="text-sm font-medium">Password</label>
              <input
                className="w-full border rounded-lg p-2"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="minimum 8 characters"
              />

              <label className="text-sm font-medium">
                What do you want to do?
              </label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value as "buyer" | "seller")}
                className="w-full border rounded-lg p-2"
              >
                <option value="buyer">Buy</option>
                <option value="seller">Sell</option>
              </select>

              <button
                className="w-full bg-black text-white rounded-lg p-2 disabled:opacity-60"
                onClick={onRegister}
                disabled={loading}
              >
                {loading ? "Creating..." : "Create account"}
              </button>
            </>
          )}

          {msg && <p className="text-sm text-blue-700">{msg}</p>}
        </div>
      </div>
    </Container>
  );
}
