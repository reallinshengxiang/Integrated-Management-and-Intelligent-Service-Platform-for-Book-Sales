import {defineConfig, loadEnv} from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path-browserify'


// https://vitejs.dev/config/
export default ({mode}) => {
  const env = loadEnv(mode, process.cwd());
  return defineConfig({
    plugins: [
      vue(),
    ],

    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `@import "@/assets/scss/global.scss";`
        }
      }
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '/src')
      },
    },
    server: {
      port: 3000,
    
      proxy: {
        '/api': {
          target: env.VITE_APP_SERVER_URL,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    },
    build:{

      rollupOptions: {
        output:{
          manualChunks(id) {
            if (id.includes('node_modules')) {
              return id.toString().split('node_modules/')[1].split('/')[0].toString();
            }
          }
        }
      }

    }

  })
}