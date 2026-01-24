import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Container from "../components/Container";
import { getProduct, updateProduct, uploadProductImage } from "../api/products";

export default function EditProduct() {
  const { id } = useParams<{ id: string }>();
  const nav = useNavigate();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [uploadingImg, setUploadingImg] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [form, setForm] = useState({
    title: "",
    description: "",
    price: 0,
    category_id: "general",
    image: "", // images[0]
  });

  useEffect(() => {
    if (!id) return;

    (async () => {
      try {
        setLoading(true);
        setError(null);

        const p = await getProduct(id);

        setForm({
          title: p.title || "",
          description: p.description || "",
          price: Number((p as any).price || 0),
          category_id: (p as any).category_id || "general",
          image: (p as any)?.images?.[0] || "",
        });
      } catch (e: any) {
        setError(e?.response?.data?.detail ?? e?.message ?? "Error cargando producto");
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  const previewSrc = useMemo(() => {
    if (!form.image) return "/no-image.png";
    if (form.image.startsWith("http")) return form.image;
    return `http://localhost:8000${form.image}`;
  }, [form.image]);

  const onPickImage = async (file: File | null) => {
    if (!file) return;
    try {
      setUploadingImg(true);
      setError(null);

      const url = await uploadProductImage(file);
      setForm((s) => ({ ...s, image: url }));
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? e?.message ?? "Error subiendo imagen");
    } finally {
      setUploadingImg(false);
    }
  };

  const onSave = async () => {
    if (!id) return;

    try {
      setSaving(true);
      setError(null);

      await updateProduct(id, {
        title: form.title,
        description: form.description,
        price: Number(form.price),
        category_id: form.category_id,
        images: form.image ? [form.image] : [],
      });

      nav("/my-products");
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? e?.message ?? "Error guardando");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <Container>
        <div className="py-10">Cargando...</div>
      </Container>
    );
  }

  return (
    <Container>
      <div className="max-w-2xl mx-auto bg-white p-6 rounded shadow-sm">
        <h1 className="text-2xl font-bold mb-4">Editar producto</h1>

        {error && (
          <div className="mb-4 p-3 border border-red-300 bg-red-50 text-red-800 rounded">
            {error}
          </div>
        )}

        {/* Imagen actual + editar */}
        <div className="mb-5">
          <img
            src={previewSrc}
            alt="preview"
            className="h-56 w-full object-cover rounded bg-gray-100"
            onError={(e) => {
              (e.currentTarget as HTMLImageElement).src = "/no-image.png";
            }}
          />

          <div className="mt-3 flex items-center gap-3">
            <label className="inline-flex items-center gap-2 px-4 py-2 rounded bg-blue-600 text-white cursor-pointer">
              {uploadingImg ? "Subiendo..." : "Editar imagen"}
              <input
                type="file"
                accept="image/*"
                className="hidden"
                onChange={(e) => onPickImage(e.target.files?.[0] ?? null)}
                disabled={uploadingImg}
              />
            </label>

            {form.image && (
              <button
                className="px-4 py-2 rounded border"
                onClick={() => setForm((s) => ({ ...s, image: "" }))}
                disabled={uploadingImg}
              >
                Quitar imagen
              </button>
            )}
          </div>
        </div>

        <label className="block text-sm font-semibold mb-2">Title</label>
        <input
          className="w-full px-4 py-2 border rounded mb-4"
          value={form.title}
          onChange={(e) => setForm((s) => ({ ...s, title: e.target.value }))}
        />

        <label className="block text-sm font-semibold mb-2">Description</label>
        <textarea
          className="w-full px-4 py-2 border rounded mb-4"
          value={form.description}
          onChange={(e) => setForm((s) => ({ ...s, description: e.target.value }))}
        />

        <label className="block text-sm font-semibold mb-2">Price</label>
        <input
          type="number"
          className="w-full px-4 py-2 border rounded mb-4"
          value={form.price}
          onChange={(e) => setForm((s) => ({ ...s, price: Number(e.target.value) }))}
        />

        <label className="block text-sm font-semibold mb-2">Category ID</label>
        <input
          className="w-full px-4 py-2 border rounded mb-6"
          value={form.category_id}
          onChange={(e) => setForm((s) => ({ ...s, category_id: e.target.value }))}
          placeholder="general"
        />

        <div className="flex gap-3">
          <button
            className="flex-1 rounded bg-blue-600 py-2 text-white disabled:opacity-60"
            onClick={onSave}
            disabled={saving || uploadingImg}
          >
            {saving ? "Guardando..." : "Guardar"}
          </button>

          <button
            className="flex-1 rounded border py-2"
            onClick={() => nav("/my-products")}
            disabled={saving || uploadingImg}
          >
            Cancelar
          </button>
        </div>
      </div>
    </Container>
  );
}
