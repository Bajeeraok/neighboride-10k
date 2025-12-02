'use client';

import { useState } from 'react';

export default function Home() {
  const [email, setEmail] = useState('');
  const [magicSent, setMagicSent] = useState(false);

  const sendMagicLink = async () => {
    try {
      alert('request received')
      const res = await fetch('http://localhost:8001/auth/request-magic-link', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      if (res.ok) {
        setMagicSent(true);
      } else {
        const error= await res.status;
        alert('Errir: ' +error);
      }
    } catch (err) {
      alert('Check backend is running on port 8001');
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-900 to-purple-900 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-10 max-w-md w-full">
        <h1 className="text-4xl font-bold text-center mb-2">Neighboride</h1>
        <p className="text-center text-gray-600 mb-8">
          Charlotte Corporate Carpool — Use your work email
        </p>

        <input
          type="email"
          placeholder="name@company.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg mb-6 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          onClick={sendMagicLink}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 rounded-lg text-lg transition"
        >
          Send Magic Login Link
        </button>

        {magicSent && (
          <p className="text-green-600 text-center mt-6 font-medium">
            Magic link sent! Check your inbox
          </p>
        )}

        <div className="mt-10 text-center text-sm text-gray-500">
          Works with @wellsfargo.com • @bankofamerica.com • @charlotte.edu • and 50+ more
        </div>
      </div>
    </main>
  );
}