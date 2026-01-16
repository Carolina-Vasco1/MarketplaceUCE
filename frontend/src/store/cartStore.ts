import { create } from "zustand";

export interface CartItem {
  id: string;
  title: string;
  price: number;
  quantity: number;
  image_url?: string;
}

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
  getTotalPrice: () => number;
}

// Listen for logout event to clear cart
if (typeof window !== "undefined") {
  window.addEventListener("logout", () => {
    // Cart will be cleared through Zustand
  });
}

export const useCart = create<CartStore>((set, get) => ({
  items: [],
  addItem: (item: CartItem) => {
    const items = get().items;
    const existing = items.find((i) => i.id === item.id);
    if (existing) {
      set({
        items: items.map((i) =>
          i.id === item.id ? { ...i, quantity: i.quantity + item.quantity } : i
        ),
      });
    } else {
      set({ items: [...items, item] });
    }
  },
  removeItem: (id: string) => {
    set({ items: get().items.filter((i) => i.id !== id) });
  },
  updateQuantity: (id: string, quantity: number) => {
    if (quantity <= 0) {
      get().removeItem(id);
    } else {
      set({
        items: get().items.map((i) =>
          i.id === id ? { ...i, quantity } : i
        ),
      });
    }
  },
  clearCart: () => set({ items: [] }),
  getTotalPrice: () => {
    return get().items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  },
}));

// Listen for logout event
if (typeof window !== "undefined") {
  window.addEventListener("logout", () => {
    useCart.setState({ items: [] });
  });
}
