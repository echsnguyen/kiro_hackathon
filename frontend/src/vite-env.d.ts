/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_API_TIMEOUT: string
  readonly VITE_WS_URL: string
  readonly VITE_ENABLE_STREAMING_TRANSCRIPTION: string
  readonly VITE_ENABLE_PII_REDACTION: string
  readonly VITE_ENVIRONMENT: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
