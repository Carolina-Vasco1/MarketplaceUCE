import { useState } from "react";
import Container from "../components/Container";
import { createProduct, uploadProductImage } from "../api/products";
import { getSession } from "../auth/session";

export default function SellProduct() {
  const session = getSession();
  const seller_id = session?.user_id || "";

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState<number>(0);
  const [category_id, setCategoryId] = useState<string>("general");

  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>("");

  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);

  async function onCreate() {
    setMsg("");
    setLoading(true);

    try {
      let images: string[] = [];

      // ✅ si hay imagen, subir primero
      if (image) {
        const url = await uploadProductImage(image); // /static/xxx.jpg
        images = [url];
      }

      const p = await createProduct({
        title,
        description,
        price,
        seller_id,
        category_id,
        images, // ✅ se guarda en el backend
      });

      setMsg(`Product created: ${p.title}`);
      setTitle("");
      setDescription("");
      setPrice(0);
      setImage(null);
      setPreview("");
    } catch (e: any) {
      setMsg(e?.response?.data?.detail ?? "Unable to create product.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Container>
      <div className="max-w-xl mx-auto">
        <h1 className="text-2xl font-semibold mb-3">Publish product</h1>

        <div className="bg-white border rounded-xl p-4 space-y-3">
          <input
            className="w-full border rounded-lg p-2"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Title"
          />

          <textarea
            className="w-full border rounded-lg p-2"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Description"
          />

          <input
            className="w-full border rounded-lg p-2"
            type="number"
            value={price}
            onChange={(e) => setPrice(Number(e.target.value))}
            placeholder="Price"
          />

          <input
            className="w-full border rounded-lg p-2"
            value={category_id}
            onChange={(e) => setCategoryId(e.target.value)}
            placeholder="Category ID (ej: general)"
          />

          {/* ✅ Imagen */}
          <div className="space-y-2">
            <input
              type="file"
              accept="image/*"
              onChange={(e) => {
                const f = e.target.files?.[0] || null;
                setImage(f);
                if (f) setPreview(URL.createObjectURL(f));
                else setPreview("");
              }}
            />

            {preview && (
              <img
                src={preview}
                className="w-full h-48 object-cover rounded-lg border"
                alt="preview"
              />
            )}
          </div>

          <button
            className="w-full bg-black text-white rounded-lg p-2 disabled:opacity-60"
            onClick={onCreate}
            disabled={loading}
          >
            {loading ? "Publishing..." : "Publish"}
          </button>

          {msg && <p className="text-sm text-blue-700">{msg}</p>}
          <p className="text-xs text-gray-500">Seller ID (JWT sub): {seller_id}</p>
        </div>
      </div>
    </Container>
  );
}
