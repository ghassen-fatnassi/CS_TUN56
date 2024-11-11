import { z } from 'zod';

const envSchema = z.object({
  VITE_API_URL: z.string().url(),
  VITE_MAX_FILE_SIZE: z.string().transform(Number),
  VITE_ALLOWED_FILE_TYPES: z.string(),
  VITE_ENABLE_VIRUS_SCAN: z.string().transform((v) => v === 'true'),
  VITE_ENABLE_DEBUG: z.string().transform((v) => v === 'true').optional(),
});

type EnvType = z.infer<typeof envSchema>;

function validateEnv(): EnvType {
  try {
    return envSchema.parse(import.meta.env);
  } catch (error) {
    console.error('Invalid environment variables:', error);
    throw new Error('Invalid environment variables');
  }
}

export const env = validateEnv();