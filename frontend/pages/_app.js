import '../src/styles/globals.css'
import { useEffect } from 'react'

function MyApp({ Component, pageProps }) {
  useEffect(() => {
    // Prevent hydration issues
    if (typeof window !== 'undefined') {
      console.log('App mounted')
    }
  }, [])

  return <Component {...pageProps} />
}

export default MyApp
