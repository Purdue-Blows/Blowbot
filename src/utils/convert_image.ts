import { readFileSync } from "fs";

/// Converts an image into a buffer to be written to MongoDB
export function convert_image(image_path: string): Buffer {
  return readFileSync(image_path);
}