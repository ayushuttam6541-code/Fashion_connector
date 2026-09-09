import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { getCurrentLocation, formatDistance, isShopOpen } from '../utils/location';
import { toast } from 'sonner';

const LocationContext = createContext(null);

export const LocationProvider = ({ children }) => {
  const [location, setLocation] = useState(null);
  const [permission, setPermission] = useState('unknown');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const requestLocation = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const coords = await getCurrentLocation();
      setLocation(coords);
      setPermission('granted');
      toast.success('Location access granted');
      return coords;
    } catch (err) {
      setError(err.message);
      setPermission('denied');
      toast.error('Could not access your location. Please enable location services.');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const setManualLocation = useCallback((lat, lon) => {
    setLocation({ latitude: lat, longitude: lon });
    setPermission('manual');
    toast.success('Location set manually');
  }, []);

  const clearLocation = useCallback(() => {
    setLocation(null);
    setPermission('unknown');
  }, []);

  // Check location permission on mount
  useEffect(() => {
    const checkPermission = async () => {
      if (navigator.permissions) {
        try {
          const result = await navigator.permissions.query({ name: 'geolocation' });
          setPermission(result.state);
          
          if (result.state === 'granted') {
            requestLocation();
          }
        } catch (e) {
          console.log('Permission check failed:', e);
        }
      }
    };
    
    checkPermission();
  }, [requestLocation]);

  const value = {
    location,
    permission,
    loading,
    error,
    requestLocation,
    setManualLocation,
    clearLocation,
    formatDistance,
    isShopOpen
  };

  return (
    <LocationContext.Provider value={value}>
      {children}
    </LocationContext.Provider>
  );
};

export const useLocation = () => {
  const context = useContext(LocationContext);
  if (!context) {
    throw new Error('useLocation must be used within LocationProvider');
  }
  return context;
};
