/**
 * API configuration
 * Exports environment-based API URL
 */

import { environment } from '../../../environments/environment';

/**
 * Base API URL from environment
 * Points to '/api' which is proxied to http://localhost:8000
 */
export const API_BASE_URL = environment.apiUrl;
