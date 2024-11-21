import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

interface DataReading {
  id: string
  weather_station_id: string
  value: number
  timestamp: string
}

interface SensorData {
  temperature: {
    current: DataReading
    stats: {
      avg: number
      max: number
      min: number
    }
  }
  humidity: {
    current: DataReading
    stats: {
      avg: number
      max: number
      min: number
    }
  }
  toxicGases: {
    current: DataReading
    stats: {
      avg: number
      max: number
      min: number
    }
  }
  history: {
    timestamp: string
    temperature: number
    humidity: number
    toxicGases: number
  }[]
}

export function useSensorData() {
  return useQuery<SensorData>({
    queryKey: ['sensorData'],
    queryFn: async () => {
      // Fetch current readings
      const [tempData, humidityData, gasesData] = await Promise.all([
        axios.get('/api/readings?type=temperature&limit=1'),
        axios.get('/api/readings?type=humidity&limit=1'),
        axios.get('/api/readings?type=toxic_gases&limit=1')
      ])

      // Fetch historical data for charts
      const history = await axios.get('/api/readings/history')
      const processedHistory = Array.isArray(history.data) ? history.data : [];

      // Calculate stats from historical data
      const calculateStats = (dataKey: 'temperature' | 'humidity' | 'toxicGases') => {
        const values = processedHistory.map(entry => entry[dataKey]);
        return {
          avg: values.reduce((sum, val) => sum + val, 0) / values.length || 0,
          max: Math.max(...values, 0),
          min: Math.min(...values, 0)
        };
      };

      const temperatureStats = calculateStats('temperature');
      const humidityStats = calculateStats('humidity');
      const toxicGasesStats = calculateStats('toxicGases');

      return {
        temperature: {
          current: tempData.data[0],
          stats: temperatureStats
        },
        humidity: {
          current: humidityData.data[0],
          stats: humidityStats
        },
        toxicGases: {
          current: gasesData.data[0],
          stats: toxicGasesStats
        },
        history: processedHistory
      }
    },
    refetchInterval: 30000,
  })
} 