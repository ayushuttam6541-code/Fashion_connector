/**
 * Location utility functions for GPS-based features
 */

/**
 * Get user's current location using browser Geolocation API
 * @returns {Promise<{latitude: number, longitude: number}>}
 */
export const getCurrentLocation = () => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation is not supported by your browser'));
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        });
      },
      (error) => {
        reject(error);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000 // 5 minutes cache
      }
    );
  });
};

/**
 * Calculate distance between two coordinates using Haversine formula
 * @param {number} lat1 - Latitude of first point
 * @param {number} lon1 - Longitude of first point
 * @param {number} lat2 - Latitude of second point
 * @param {number} lon2 - Longitude of second point
 * @returns {number} Distance in kilometers
 */
export const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371; // Earth's radius in km
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  
  const a = 
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
};

const toRad = (deg) => deg * (Math.PI / 180);

/**
 * Format distance for display
 * @param {number} distanceKm - Distance in kilometers
 * @returns {string} Formatted distance string
 */
export const formatDistance = (distanceKm) => {
  if (distanceKm < 1) {
    return `${Math.round(distanceKm * 1000)} m away`;
  }
  return `${distanceKm.toFixed(1)} km away`;
};

/**
 * Check if a shop is currently open based on its timings
 * @param {Object} timings - Shop timings object
 * @returns {boolean} Whether shop is open
 */
export const isShopOpen = (timings) => {
  if (!timings) return false;
  
  const now = new Date();
  const dayName = now.toLocaleDateString('en-US', { weekday: 'long' });
  const todayTiming = timings[dayName];
  
  if (!todayTiming || todayTiming === 'Closed') return false;
  
  try {
    const [openTime, closeTime] = todayTiming.split(' - ');
    const openMinutes = timeToMinutes(openTime);
    const closeMinutes = timeToMinutes(closeTime);
    const currentMinutes = now.getHours() * 60 + now.getMinutes();
    
    return currentMinutes >= openMinutes && currentMinutes <= closeMinutes;
  } catch (e) {
    return false;
  }
};

/**
 * Convert time string to minutes since midnight
 * @param {string} timeStr - Time string like "11:00 AM"
 * @returns {number} Minutes since midnight
 */
const timeToMinutes = (timeStr) => {
  const [time, period] = timeStr.trim().split(' ');
  let [hours, minutes] = time.split(':').map(Number);
  
  if (period === 'PM' && hours !== 12) {
    hours += 12;
  } else if (period === 'AM' && hours === 12) {
    hours = 0;
  }
  
  return hours * 60 + minutes;
};

/**
 * Get location permission status
 * @returns {Promise<string>} Permission status
 */
export const getLocationPermission = async () => {
  if (!navigator.permissions) {
    return 'unknown';
  }
  
  try {
    const result = await navigator.permissions.query({ name: 'geolocation' });
    return result.state;
  } catch (e) {
    return 'unknown';
  }
};

/**
 * Request location permission
 * @returns {Promise<{latitude: number, longitude: number}>}
 */
export const requestLocationPermission = async () => {
  try {
    return await getCurrentLocation();
  } catch (error) {
    throw new Error('Location permission denied');
  }
};