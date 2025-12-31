"""
Configuración de Tailwind CSS para Thermomix TM6
Incluye CDN, tema personalizado y estilos globales
"""

def get_tailwind_cdn():
    """
    Retorna el HTML completo para inyectar Tailwind CSS CDN + configuración personalizada

    Returns:
        str: HTML con script de Tailwind, configuración y fuentes
    """
    return '''
    <!-- Tailwind CSS CDN v3.4 -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Configuración de Tailwind personalizada para Thermomix -->
    <script>
        tailwind.config = {
            darkMode: 'class',  // Habilita modo oscuro con clase en <html>
            theme: {
                extend: {
                    colors: {
                        // Paleta Thermomix TM6 Professional
                        'thermo-navy': {
                            50: '#f0f4f8',
                            100: '#d9e2ec',
                            200: '#bcccdc',
                            300: '#9fb3c8',
                            400: '#829ab1',
                            500: '#627d98',  // Navy principal
                            600: '#486581',
                            700: '#334e68',
                            800: '#243b53',
                            900: '#102a43',
                            950: '#0d1f2f',
                        },
                        'thermo-cyan': {
                            50: '#e0f7ff',
                            100: '#b3ebff',
                            200: '#80deff',
                            300: '#4dd1ff',
                            400: '#26c7ff',
                            500: '#06b6d4',  // Cyan principal
                            600: '#0891b2',
                            700: '#0e7490',
                            800: '#155e75',
                            900: '#164e63',
                        },
                        'thermo-green': '#00ff88',
                        'thermo-magenta': '#ff006e',
                        'thermo-orange': '#ff9500',
                        'thermo-red': '#ff3b3b',
                    },
                    fontFamily: {
                        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
                        mono: ['Fira Code', 'Consolas', 'Monaco', 'Courier New', 'monospace'],
                    },
                    boxShadow: {
                        'glow-cyan': '0 0 30px rgba(6, 182, 212, 0.5)',
                        'glow-green': '0 0 30px rgba(0, 255, 136, 0.5)',
                        'glow-red': '0 0 30px rgba(255, 0, 110, 0.5)',
                        'glow-orange': '0 0 30px rgba(255, 149, 0, 0.5)',
                    },
                    animation: {
                        'pulse-glow': 'pulse-glow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                        'led-pulse': 'led-pulse 1.5s ease-in-out infinite',
                        'fade-in': 'fade-in 0.3s ease-out',
                        'slide-up': 'slide-up 0.4s ease-out',
                    },
                    keyframes: {
                        'pulse-glow': {
                            '0%, 100%': {
                                boxShadow: '0 0 20px rgba(6, 182, 212, 0.4)',
                                transform: 'scale(1)'
                            },
                            '50%': {
                                boxShadow: '0 0 40px rgba(6, 182, 212, 0.7)',
                                transform: 'scale(1.02)'
                            },
                        },
                        'led-pulse': {
                            '0%, 100%': { opacity: '1' },
                            '50%': { opacity: '0.6' },
                        },
                        'fade-in': {
                            '0%': { opacity: '0' },
                            '100%': { opacity: '1' },
                        },
                        'slide-up': {
                            '0%': {
                                opacity: '0',
                                transform: 'translateY(20px)'
                            },
                            '100%': {
                                opacity: '1',
                                transform: 'translateY(0)'
                            },
                        },
                    },
                }
            }
        }
    </script>

    <!-- Google Fonts: Inter y Fira Code -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Fira+Code:wght@400;500;600&display=swap" rel="stylesheet">

    <!-- Estilos CSS Globales -->
    <style>
        /* === TRANSICIONES SUAVES === */
        * {
            transition-property: background-color, border-color, color, fill, stroke, opacity, transform;
            transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
            transition-duration: 200ms;
        }

        /* === SCROLLBAR PERSONALIZADO === */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #e5e7eb;
            border-radius: 5px;
        }

        .dark ::-webkit-scrollbar-track {
            background: #1f2937;
        }

        ::-webkit-scrollbar-thumb {
            background: #9ca3af;
            border-radius: 5px;
            transition: background 0.2s ease;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #06b6d4;
        }

        /* === UTILIDADES DE LÍNEA === */
        .line-clamp-1 {
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .line-clamp-2 {
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .line-clamp-3 {
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        /* === GLASS-MORPHISM === */
        .glass {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .glass-dark {
            background: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* === ANIMACIÓN DE CARGA === */
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .spin {
            animation: spin 1s linear infinite;
        }

        /* === EFECTO RIPPLE EN BOTONES === */
        @keyframes ripple {
            0% {
                transform: scale(0);
                opacity: 1;
            }
            100% {
                transform: scale(4);
                opacity: 0;
            }
        }

        /* === FOCUS VISIBLE === */
        *:focus-visible {
            outline: 2px solid #06b6d4;
            outline-offset: 2px;
        }

        /* === SMOOTH SCROLL === */
        html {
            scroll-behavior: smooth;
        }

        /* === BODY BASE === */
        body {
            margin: 0;
            padding: 0;
            min-height: 100vh;
            font-family: 'Inter', sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* === NICEGUI OVERRIDES === */
        .nicegui-content {
            width: 100% !important;
            max-width: 100% !important;
            padding: 0 !important;
        }

        /* === QUASAR CARD RESET === */
        .q-card {
            box-shadow: none;
        }

        /* === TOOLTIPS MEJORADOS === */
        .q-tooltip {
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(8px);
            font-size: 0.875rem;
            padding: 0.5rem 0.75rem;
            border-radius: 0.5rem;
        }
    </style>
    '''


def get_dark_mode_init_script():
    """
    Script para inicializar el modo oscuro antes de que se renderice la página
    Previene el "flash" de contenido en modo claro

    Returns:
        str: HTML con script de inicialización
    """
    return '''
    <script>
        // Restaurar preferencia de modo oscuro ANTES de renderizar
        (function() {
            const darkMode = localStorage.getItem('thermomix_dark_mode') === 'true';
            if (darkMode) {
                document.documentElement.classList.add('dark');
            }
        })();
    </script>
    '''


def get_meta_tags():
    """
    Meta tags para SEO y PWA

    Returns:
        str: HTML con meta tags
    """
    return '''
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="description" content="Robot de Cocina Thermomix TM6 - Control Inteligente">
    <meta name="author" content="Robot de Cocina">
    <meta name="theme-color" content="#06b6d4">
    <title>Thermomix TM6 | Control Inteligente</title>
    '''


def inject_all_styles():
    """
    Función de conveniencia que inyecta todos los estilos necesarios

    Returns:
        str: HTML completo con todos los estilos
    """
    return (
        get_meta_tags() +
        get_dark_mode_init_script() +
        get_tailwind_cdn()
    )
