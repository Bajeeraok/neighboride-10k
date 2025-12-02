'use client';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';
import axios from 'axios';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

function CheckoutForm({ amount }: { amount: number }) {
  const stripe = useStripe();
  const elements = useElements();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!stripe || !elements) return;

    const { data: { clientSecret } } = await axios.post('/api/bookings', { /* booking data */ });
    const result = await stripe.confirmCardPayment(clientSecret, {
      payment_method: { card: elements.getElement(CardElement)! }
    });
    if (result.error) alert(result.error.message);
  };

  return (
    <form onSubmit={handleSubmit}>
      <CardElement />
      <button type="submit" className="bg-green-500 text-white px-4 py-2 mt-4">Pay ${amount}</button>
    </form>
  );
}

export default function BookPage({ params }: { params: { id: string } }) {
  return (
    <Elements stripe={stripePromise}>
      <CheckoutForm amount={25} /> {/* Example */}
    </Elements>
  );
}