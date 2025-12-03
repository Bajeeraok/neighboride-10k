// web/app/page.tsx — FINAL CUTTING-EDGE NEIGHBORIDE UI (2025)
'use client';

import { useState } from 'react';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { Car, Users, Zap, Mail, ArrowRight, CheckCircle } from 'lucide-react';

export default function Home() {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);

  const sendMagicLink = async () => {
    if (!email.includes('@')) return;
    setLoading(true);
    try {
      await fetch('http://localhost:8001/auth/request-magic-link', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email.toLowerCase().trim() }),
      });
      setSent(true);
    } catch (e) {
      alert('Backend not reachable');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Dynamic Charlotte Skyline Background */}
      <div className="fixed inset-0 -z-10 overflow-hidden">
        <Image
          src="https://images.unsplash.com/photo-1598387993426-9e83a1d27892?w=1920&q=80"
          alt="Charlotte skyline at golden hour"
          fill
          priority
          className="object-cover brightness-75 scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-blue-950/90 via-purple-900/70 to-black/80" />
      </div>

      <main className="min-h-screen flex items-center justify-center px-6 relative">
        <div className="max-w-5xl w-full grid md:grid-cols-2 gap-16 items-center">
          {/* LEFT: Hero Content */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-white"
          >
            <h1 className="text-7xl md:text-8xl font-black tracking-tighter mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
              Neighboride
            </h1>
            <p className="text-3xl md:text-4xl font-light mb-6 text-blue-100">
              Charlotte’s Corporate Carpool
            </p>
            <p className="text-xl text-gray-200 leading-relaxed mb-10 max-w-lg">
              Skip I-77 traffic. Ride with coworkers from{' '}
              <span className="font-bold text-blue-300">Wells Fargo</span>,{' '}
              <span className="font-bold text-green-300">Bank of America</span>,{' '}
              <span className="font-bold text-yellow-300">Lowe’s</span>, and 50+ more.
            </p>

            <div className="flex gap-8 text-gray-300">
              <div className="flex items-center gap-3">
                <Car className="w-8 h-8 text-blue-400" />
                <span className="text-lg">Save $400+/month</span>
              </div>
              <div className="flex items-center gap-3">
                <Users className="w-8 h-8 text-purple-400" />
                <span className="text-lg">Verified coworkers only</span>
              </div>
              <div className="flex items-center gap-3">
                <Zap className="w-8 h-8 text-yellow-400" />
                <span className="text-lg">Real-time matching</span>
              </div>
            </div>
          </motion.div>

          {/* RIGHT: Glassmorphic Login Card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="backdrop-blur-2xl bg-white/10 border border-white/20 rounded-3xl p-10 shadow-3xl"
          >
            {!sent ? (
              <>
                <div className="flex items-center gap-3 mb-8">
                  <div className="p-3 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl">
                    <Mail className="w-8 h-8 text-white" />
                  </div>
                  <div>
                    <h2 className="text-3xl font-bold text-white">Welcome back</h2>
                    <p className="text-gray-300">Sign in with your work email</p>
                  </div>
                </div>

                <input
                  type="email"
                  placeholder="you@bankofamerica.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && sendMagicLink()}
                  className="w-full px-6 py-5 bg-white/20 border border-white/30 rounded-2xl text-white placeholder-gray-400 text-lg focus:outline-none focus:ring-4 focus:ring-blue-500/50 transition-all"
                />

                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={sendMagicLink}
                  disabled={loading || !email.includes('@')}
                  className="mt-6 w-full py-5 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-bold text-xl rounded-2xl flex items-center justify-center gap-3 transition-all shadow-2xl"
                >
                  {loading ? (
                    'Sending...'
                  ) : (
                    <>
                      Send Magic Link
                      <ArrowRight className="w-6 h-6" />
                    </>
                  )}
                </motion.button>

                <p className="mt-6 text-gray-400 text-center text-sm">
                  Works with 50+ Charlotte companies including Wells Fargo, Truist, Atrium Health, UNC Charlotte
                </p>
              </>
            ) : (
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="text-center py-10"
              >
                <CheckCircle className="w-24 h-24 text-green-400 mx-auto mb-6" />
                <h3 className="text-3xl font-bold text-white mb-4">Check your email</h3>
                <p className="text-xl text-gray-300">
                  Magic link sent to <span className="text-blue-300 font-bold">{email}</span>
                </p>
                <p className="text-gray-400 mt-4">Click the link to log in instantly</p>
              </motion.div>
            )}
          </motion.div>
        </div>

        {/* Floating Trust Badges */}
        <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex gap-8 opacity-70">
          {['Wells Fargo', 'Bank of America', 'Truist', 'Lowe’s', 'UNC Charlotte'].map((name) => (
            <div key={name} className="px-6 py-3 bg-white/10 backdrop-blur-lg rounded-full text-white text-sm font-medium border border-white/20">
              {name}
            </div>
          ))}
        </div>
      </main>
    </>
  );
}
