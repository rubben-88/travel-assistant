interface ImportMetaEnv {
    VITE_SENDQUERY_URI: string;
    VITE_CHECKSESSIONID_URI: string;
    VITE_FRESHSESSIONID_URI: string;
}
  
interface ImportMeta {
    readonly env: ImportMetaEnv;
}