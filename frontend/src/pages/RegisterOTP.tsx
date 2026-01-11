import { useState } from "react";
import Container from "../components/Container";
import { requestOtp, verifyOtp, register } from "../api/auth";
import { setToken } from "../auth/token";
import { useNavigate } from "react-router-dom";

type Role = "buyer" | "seller";

export default function RegisterOTP() {
  const nav = useNavigate();
  const [step, setStep] = useState<1 | 2 | 3>(1);

  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<Role>("buyer");

  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);

  function normalizeEmail(v: string) {
    return v.trim().toLowerCase();
  }

  function isInstitutionalEmail(v: string) {
    return /^[a-z0-9._%+-]+@uce\.edu\.ec$/i.test(v.trim());
  }

  async function onRequestOTP() {
    setMsg("");
    setLoading(true);
    try {
      const em = normalizeEmail(email);
      if (!isInstitutionalEmail(em)) {
        throw new Error("Use un correo institucional válido @uce.edu.ec");
      }

      await requestOtp(em);
      setEmail(em);
      setStep(2);
      setMsg("OTP sent. Check your institutional email.");
    } catch (e: any) {
      setMsg(e?.response?.data?.detail ?? e?.message ?? "Error requesting OTP");
    } finally {
      setLoading(false);
    }
  }

  async function onVerifyOTP() {
    setMsg("");
    setLoading(true);
    try {
      const em = normalizeEmail(email);
      const otp = code.trim();

      if (!/^\d{6}$/.test(otp)) {
        throw new Error("El OTP debe tener 6 dígitos.");
      }

      await verifyOtp(em, otp);
      setEmail(em);
      setCode(otp);
      setStep(3);
      setMsg("Email verified. You can now register.");
    } catch (e: any) {
      setMsg(e?.response?.data?.detail ?? e?.message ?? "Invalid OTP");
    } finally {
      setLoading(false);
    }
  }

  async function onRegister() {
    setMsg("");
    setLoading(true);
    try {
      const em = normalizeEmail(email);

      if (!isInstitutionalEmail(em)) {
        throw new Error("Use un correo institucional válido @uce.edu.ec");
      }
      if (password.length < 8) {
        throw new Error("La contraseña debe tener al menos 8 caracteres.");
      }
      // bcrypt: 72 bytes
      if (new TextEncoder().encode(password).length > 72) {
        throw new Error("La contraseña es muy larga (máx. 72 bytes).");
      }

      const r = await register(em, password, role);
      setToken(r.access_token);
      nav("/");
    } catch (e: any) {
      setMsg(e?.response?.data?.detail ?? e?.message ?? "Registration error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Container>
      <div className="max-w-lg mx-auto">
        <h1 className="text-2xl font-semibold mb-3">
          Register with OTP (@uce.edu.ec)
        </h1>

        <div className="bg-white border rounded-xl p-4 space-y-3">
          {step === 1 && (
            <>
              <label className="text-sm font-medium">Institutional email</label>
              <input
                className="w-full border rounded-lg p-2"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@uce.edu.ec"
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
                onChange={(e) => {
                  // solo números y máximo 6
                  const onlyDigits = e.target.value.replace(/\D/g, "").slice(0, 6);
                  setCode(onlyDigits);
                }}
                placeholder="6 digits"
                inputMode="numeric"
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
                onChange={(e) => setRole(e.target.value as Role)}
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
