interface ImportMetaEnv {
    readonly VITE_API_URL: string;
    readonly VITE_MAX_FILE_SIZE: string;
    readonly VITE_ALLOWED_FILE_TYPES: string;
    readonly VITE_ENABLE_VIRUS_SCAN: string;
    readonly VITE_ENABLE_DEBUG?: string;
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
  