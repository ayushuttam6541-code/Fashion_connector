import { Link } from "react-router-dom";
import { XCircle } from "lucide-react";
import { Button } from "../components/ui/button";

export default function PaymentCancelPage() {
  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white border border-slate-200 rounded-2xl p-10 text-center">
        <XCircle className="w-14 h-14 mx-auto text-amber-600" />
        <h1 className="font-display text-2xl font-bold mt-4">Payment cancelled</h1>
        <p className="text-slate-600 mt-2 text-sm">Your items are still in your cart. You can try again anytime.</p>
        <div className="flex gap-2 justify-center mt-6">
          <Link to="/cart"><Button className="bg-orange-700 hover:bg-orange-800 rounded-full">Back to Cart</Button></Link>
          <Link to="/"><Button variant="outline" className="rounded-full">Home</Button></Link>
        </div>
      </div>
    </div>
  );
}
