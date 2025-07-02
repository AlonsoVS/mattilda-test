// Re-export everything from the new API structure
export * from './api/index';

// For backward compatibility, import and re-export the default
import * as apiModules from './api/index';
export default apiModules;
