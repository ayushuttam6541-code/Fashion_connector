import { createContext, useContext, useEffect, useState } from "react";

const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [items, setItems] = useState(() => {
    try { return JSON.parse(localStorage.getItem("fc_cart") || "[]"); } catch { return []; }
  });

  useEffect(() => {
    localStorage.setItem("fc_cart", JSON.stringify(items));
  }, [items]);

  const add = (product, qty = 1) => {
    setItems((prev) => {
      const idx = prev.findIndex((i) => i.product_id === product.id);
      if (idx >= 0) {
        const copy = [...prev];
        copy[idx] = { ...copy[idx], quantity: copy[idx].quantity + qty };
        return copy;
      }
      return [...prev, { product_id: product.id, name: product.name,
                         price: product.price, image_url: product.image_url,
                         shop_id: product.shop_id, quantity: qty }];
    });
  };
  const remove = (pid) => setItems((prev) => prev.filter((i) => i.product_id !== pid));
  const setQty = (pid, qty) => setItems((prev) => prev.map((i) => i.product_id === pid ? { ...i, quantity: Math.max(1, qty) } : i));
  const clear = () => setItems([]);
  const count = items.reduce((s, i) => s + i.quantity, 0);
  const total = items.reduce((s, i) => s + i.price * i.quantity, 0);

  return (
    <CartContext.Provider value={{ items, add, remove, setQty, clear, count, total }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => useContext(CartContext);
