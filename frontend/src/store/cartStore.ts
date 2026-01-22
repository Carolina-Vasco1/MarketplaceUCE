import { create } from "zustand";
import { persist, createJSONStorage, type StateStorage } from "zustand/middleware";

export type CartItem = {
  id: string;
  title: string;
  price: number;
  quantity: number;
  image_url?: string;
};

const normUid = (userId?: string) => (userId && userId.trim() ? userId.trim() : "guest");
const cartKey = (userId?: string) => `cart:${normUid(userId)}`;

// ✅ formato real que guarda zustand/persist en storage JSON
type PersistedValue = {
  state?: { items?: CartItem[] };
  version?: number;
};

type CartState = {
  userId?: string;
  items: CartItem[];

  setUser: (userId?: string) => void;

  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, qty: number) => void;
  clearCart: () => void;
  getTotalPrice: () => number;
};

// ✅ puntero global para storage dinámico (sin auto-referencia a useCart)
let currentUserId: string = "guest";

const storage: StateStorage = {
  getItem: (_name: string): string | null => localStorage.getItem(cartKey(currentUserId)),
  setItem: (_name: string, value: string): void => localStorage.setItem(cartKey(currentUserId), value),
  removeItem: (_name: string): void => localStorage.removeItem(cartKey(currentUserId)),
};

function readPersistedItems(uid?: string): CartItem[] {
  const raw = localStorage.getItem(cartKey(uid));
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw) as PersistedValue;
    return parsed?.state?.items ?? [];
  } catch {
    return [];
  }
}

function writePersistedItems(uid: string, items: CartItem[]) {
  const value: PersistedValue = { state: { items }, version: 0 };
  localStorage.setItem(cartKey(uid), JSON.stringify(value));
}

function mergeItems(a: CartItem[], b: CartItem[]): CartItem[] {
  const map = new Map<string, CartItem>();
  for (const it of a) map.set(it.id, { ...it });

  for (const it of b) {
    const ex = map.get(it.id);
    if (ex) map.set(it.id, { ...ex, quantity: ex.quantity + it.quantity });
    else map.set(it.id, { ...it });
  }
  return Array.from(map.values());
}

export const useCart = create<CartState>()(
  persist(
    (set, get) => ({
      userId: "guest",
      items: [],

      setUser: (userId) => {
        const prevUid = currentUserId;
        const nextUid = normUid(userId);

        // 1) cambia puntero del storage
        currentUserId = nextUid;

        // 2) carga items persistidos
        const guestItems = readPersistedItems("guest");
        const nextItems = readPersistedItems(nextUid);

        // 3) migración guest -> user con merge
        if (prevUid === "guest" && nextUid !== "guest" && guestItems.length > 0) {
          const merged = mergeItems(nextItems, guestItems);

          writePersistedItems(nextUid, merged);
          localStorage.removeItem(cartKey("guest"));

          set({ userId: nextUid, items: merged });
          return;
        }

        // 4) normal: solo cargar el carrito del usuario actual
        set({ userId: nextUid, items: nextItems });
      },

      addItem: (item) =>
        set((state) => {
          const existing = state.items.find((i) => i.id === item.id);
          if (existing) {
            return {
              items: state.items.map((i) =>
                i.id === item.id ? { ...i, quantity: i.quantity + item.quantity } : i
              ),
            };
          }
          return { items: [...state.items, item] };
        }),

      removeItem: (id) => set((state) => ({ items: state.items.filter((i) => i.id !== id) })),

      updateQuantity: (id, qty) =>
        set((state) => ({
          items: state.items.map((i) => (i.id === id ? { ...i, quantity: qty } : i)),
        })),

      clearCart: () => set({ items: [] }),

      getTotalPrice: () => get().items.reduce((acc, i) => acc + i.price * i.quantity, 0),
    }),
    {
      name: "marketplaceuce-cart",
      storage: createJSONStorage(() => storage),
      partialize: (state) => ({ items: state.items }),
    }
  )
);
