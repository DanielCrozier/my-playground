/// <reference types="vite/client" />

// Declare process.env fields that are statically replaced by Vite's `define`.
// This shim exists for TypeScript only; Vite replaces the references at build time.
declare const process: {
  env: {
    VITE_API_BASE_URL?: string;
  };
};
