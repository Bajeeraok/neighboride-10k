'use client';
import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [magicSent, setMagicSent] = useState(false);

  const sendMagicLink = async () => {
    await axios.post('/api/auth/request-magic-link', { email });
    setMagicSent(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-purple-900 flex items-center justify-center">
      <div className="bg-white p-10 rounded-2xl shadow-2xl max-w-md w-full">
        <h1 className="text-4xl font-bold text-center mb-8">Neighboride</h1>
        <p className="text-center text-gray-600 mb-8">
          Charlotte Corporate Carpool • Use your work email
        </p>

        <input
          type="email"
          placeholder="name@company.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-4 border rounded-lg mb-4 text-lg"
        />

        <input
          type="password"
          placeholder="Password (optional)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-4 border rounded-lg mb-6 text-lg"
        />

        <button
          onClick={sendMagicLink}
          className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold text-lg hover:bg-blue-700"
        >
          Send Magic Login Link
        </button>

        {magicSent && (
          <p className="text-green-600 text-center mt-4">
            Check your inbox — link sent to {email}
          </p>
        )}

        <div className="mt-8 text-center text-sm text-gray-500">
          Approved domains: @wellsfargo.com • @bankofamerica.com • @charlotte.edu • and 50+ more
        </div>
      </div>
    </div>
  );
}