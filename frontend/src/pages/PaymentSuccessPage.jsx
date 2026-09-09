import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { CheckCircle2, XCircle, Loader2 } from "lucide-react";
import api from "../lib/api";
import { Button } from "../components/ui/button";
import { useCart } from "../context/CartContext";

export default function PaymentSuccessPage() {
  const [params] = useSearchParams();
  const sid = params.get("session_id");
  const [status, setStatus] = useState("polling");
  const { clear } = useCart();

  useEffect(() => {
    if (!sid) return;
    let attempts = 0;
    const timer = setInterval(async () => {
      attempts++;
      try {
        const { data } = await api.get(`/api/payments/status/${sid}`);
        if (data.payment_status === "paid") {
          setStatus("paid");
          clear();
          clearInterval(timer);
        } else if (["failed", "expired"].includes(data.payment_status)) {
          setStatus("failed"); clearInterval(timer);
        }
      } catch {}
      if (attempts >= 15) { setStatus("timeout"); clearInterval(timer); }
    }, 2000);
    return () => clearInterval(timer);
    // eslint-disable-next-line
  }, [sid]);

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white border border-slate-200 rounded-2xl p-10 text-center">
        {status === "polling" && (<>
          <Loader2 className="w-14 h-14 mx-auto text-orange-700 animate-spin" />
          <h1 className="font-display text-2xl font-bold mt-4">Confirming your payment...</h1>
          <p className="text-slate-600 mt-2 text-sm">Hold on, this usually takes a few seconds.</p>
        </>)}
        {status === "paid" && (<>
          <CheckCircle2 className="w-14 h-14 mx-auto text-emerald-600" />
          <h1 className="font-display text-2xl font-bold mt-4">Payment successful!</h1>
          <p className="text-slate-600 mt-2 text-sm">Thank you for shopping with FashionConnect. Your order is confirmed.</p>
          <Link to="/shops"><Button className="mt-6 bg-slate-900 hover:bg-slate-800 rounded-full">Continue Shopping</Button></Link>
        </>)}
        {status === "failed" && (<>
          <XCircle className="w-14 h-14 mx-auto text-red-600" />
          <h1 className="font-display text-2xl font-bold mt-4">Payment failed</h1>
          <p className="text-slate-600 mt-2 text-sm">Something went wrong. Please try again.</p>
          <Link to="/cart"><Button className="mt-6 bg-orange-700 hover:bg-orange-800 rounded-full">Back to Cart</Button></Link>
        </>)}
        {status === "timeout" && (<>
          <h1 className="font-display text-2xl font-bold mt-4">Still processing...</h1>
          <p className="text-slate-600 mt-2 text-sm">We're still confirming your payment. Please check your orders in a few minutes.</p>
          <Link to="/"><Button className="mt-6 rounded-full">Go Home</Button></Link>
        </>)}
      </div>
    </div>
  );
}
