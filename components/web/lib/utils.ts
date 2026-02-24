import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Utility function to merge Tailwind CSS classes with proper precedence handling.
 * Combines clsx for conditional classes with twMerge for Tailwind specificity.
 *
 * @param inputs - ClassValue[] array of class names, objects, or arrays
 * @returns Merged class name string
 *
 * @example
 * cn("px-4 py-2", "px-8")  // "px-8 py-2" (px-8 overrides px-4)
 * cn("px-4", { "py-2": true, "text-red-500": false })  // "px-4 py-2"
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
