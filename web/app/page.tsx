'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import { motion, useScroll, useTransform } from 'framer-motion';
import { Car, Users, Zap, Mail, ArrowRight, CheckCircle, Sparkles } from 'lucide-react';

// CRITICAL FIX: Input works on Railway/Vercel
export const dynamic = 'force-dynamic';

export default function Home() {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);

  const { scrollY } = useScroll();
  const yBg = useTransform(scrollY, [0, 1000], [0, -200]); // Parallax sky
  const yCar = useTransform(scrollY, [0, 800], [100, -400]); // Flying car effect

  const sendMagicLink = async () => {
    if (!email.includes('@')) return;
    setLoading(true);
    try {
      await fetch('/api/auth/request-magic-link', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email.toLowerCase().trim() }),
      });
      setSent(true);
    } catch (e) {
      alert('Backend not reachable — are you running the backend?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Animated Charlotte Uptown Background */}
      <motion.div style={{ y: yBg }} className="fixed inset-0 -z-10">
        <Image
          src="https://images.unsplash.com/photo-1598387993426-9e83a1d27892?w=1920&q=85"
          alt="Charlotte Uptown skyline at golden hour"
          fill
          priority
          className="object-cover brightness-90"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-blue-950/80 via-purple-900/60 to-cyan-900/70" />
      </motion.div>

      {/* Floating Animated Car with Happy Coworkers */}
      <motion.div
        style={{ y: yCar }}
        animate={{
          x: [0, 40, -30, 0],
          rotate: [0, 3, -2, 0],
        }}
        transition={{
          x: { duration: 20, repeat: Infinity, ease: "linear" },
          rotate: { duration: 12, repeat: Infinity, ease: "easeInOut" },
        }}
        className="fixed top-32 right-10 z-20 hidden lg:block"
      >
        <div className="relative">
          <motion.div
            animate={{ rotate: [0, 360] }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="absolute -top-4 -left-8 text-yellow-400"
          >
            <Sparkles className="w-12 h-12 drop-shadow-lg" />
          </motion.div>
          <Image
            src="https://res.cloudinary.com/dca1x7vme/image/upload/v1735800000/car-happy-people-transparent_zk5vns.png"
            alt="Happy coworkers carpooling in Charlotte"
            width={420}
            height={240}
            className="drop-shadow-2xl"
            priority
          />
          <motion.div
            animate={{ y: [0, -8, 0] }}
            transition={{ duration: 3, repeat: Infinity }}
            className="absolute -bottom-4 left-1/2 -translate-x-1/2 bg-white/90 backdrop-blur px-6 py-2 rounded-full text-purple-700 font-bold text-sm shadow-lg"
          >
            Just saved $47 this week!
          </motion.div>
        </div>
      </motion.div>

      <main className="min-h-screen flex items-center justify-center px-6 relative overflow-hidden">
        <div className="max-w-7xl w-full grid lg:grid-cols-2 gap-16 items-center">

          {/* LEFT: Hero */}
          <motion.div
            initial={{ opacity: 0, y: 60 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, ease: "easeOut" }}
            className="text-white"
          >
            <motion.h1
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.9, delay: 0.2 }}
              className="text-7xl md:text-8xl lg:text-9xl font-black tracking-tighter mb-6 bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 via-blue-400 to-purple-500"
            >
              Neighboride
            </motion.h1>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="text-3xl md:text-5xl font-light mb-8 text-cyan-100"
            >
              Charlotte’s <span className="font-bold text-yellow-300">Smartest</span> Carpool
            </motion.p>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
              className="text-xl md:text-2xl text-gray-200 leading-relaxed mb-12 max-w-2xl"
            >
              Ditch I-77. Ride with verified coworkers from{' '}
              <span className="font-bold text-green-300">Bank of America</span>,{' '}
              <span className="font-bold text-blue-300">Wells Fargo</span>,{' '}
              <span className="font-bold text-purple-300">Truist</span>, and 60+ top employers.
            </motion.p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-gray-100">
              {[
                { icon: Car, text: "Save $400–$800/month", color: "text-cyan-400" },
                { icon: Users, text: "Verified coworkers only", color: "text-purple-400" },
                { icon: Zap, text: "Match & ride in < 3 min", color: "text-yellow-400" },
              ].map((item, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -40 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 1 + i * 0.2 }}
                  className="flex items-center gap-4 bg-white/10 backdrop-blur rounded-2xl p-5 border border-white/20"
                >
                  <item.icon className={`w-10 h-10 ${item.color}`} />
                  <span className="text-lg font-medium">{item.text}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* RIGHT: Glassmorphic Card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 50 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="backdrop-blur-3xl bg-white/15 border border-white/30 rounded-3xl p-10 shadow-4xl"
          >
            {!sent ? (
              <>
                <div className="flex items-center gap-4 mb-10">
                  <div className="p-4 bg-gradient-to-br from-cyan-500 to-purple-600 rounded-3xl">
                    <Mail className="w-10 h-10 text-white" />
                  </div>
                  <div>
                    <h2 className="text-4xl font-black text-white">Get Your Magic Link</h2>
                    <p className="text-xl text-cyan-200">Sign in with work email · No password</p>
                  </div>
                </div>

                <input name="email" id="email"
                  autoComplete="email"
                  autoComplete="on"
                  type="email"
                  placeholder="you@bankofamerica.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && sendMagicLink()}
                  className="w-full px-8 py-6 bg-white/20 border border-white/40 rounded-3xl text-white placeholder-gray-300 text-xl focus:outline-none focus:ring-4 focus:ring-cyan-500/60 focus:border-cyan-400 transition-all"
                />

                <motion.button
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={sendMagicLink}
                  disabled={loading || !email.includes('@')}
                  className="mt-8 w-full py-6 bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 disabled:from-gray-600 disabled:to-gray-700 text-white font-black text-2xl rounded-3xl flex items-center justify-center gap-4 transition-all shadow-2xl"
                >
                  {loading ? 'Sending Magic...' : (
                    <>
                      Send My Link <ArrowRight className="w-8 h-8" />
                    </>
                  )}
                </motion.button>

                <p className="mt-8 text-center text-gray-300 text-lg">
                  Trusted at <span className="font-bold text-cyan-300">60+ Charlotte companies</span>
                </p>
              </>
            ) : (
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="text-center py-16"
              >
                <CheckCircle className="w-32 h-32 text-green-400 mx-auto mb-8" />
                <h3 className="text-4xl font-black text-white mb-4">Check Your Inbox!</h3>
                <p className="text-2xl text-cyan-200">
                  Magic link sent to <span className="text-yellow-300 font-bold">{email}</span>
                </p>
                <p className="text-gray-300 mt-6 text-lg">Click to ride with your team today</p>
              </motion.div>
            )}
          </motion.div>
        </div>

        {/* Floating Trust Badges */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 0.8, y: 0 }}
          transition={{ delay: 1.5 }}
          className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-wrap justify-center gap-6"
        >
          {['Bank of America', 'Wells Fargo', 'Truist', 'Lowe’s', 'Atrium Health', 'UNC Charlotte'].map((name) => (
            <div
              key={name}
              className="px-6 py-3 bg-white/20 backdrop-blur-xl rounded-full text-white font-semibold border border-white/30 shadow-lg"
            >
              {name}
            </div>
          ))}
        </motion.div>
      </main>
    </>
  );
}
