import { useQuery } from '@tanstack/react-query'
import { ReadingsService, DataReading } from '../client/services'

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

export function useSensorData(refetchInterval = 5000) {
  return useQuery<SensorData>({
    queryKey: ['sensorData'],
    queryFn: async () => {
      // Get the first weather station's ID
      const weatherStations = await ReadingsService.getWeatherStations()
      const weatherStationId = weatherStations[0]?.id

      if (!weatherStationId) {
        throw new Error('No weather station found')
      }

      // Fetch current readings
      const [tempData, humidityData, gasesData] = await Promise.all([
        ReadingsService.getCurrentReadings(weatherStationId, 'temperature'),
        ReadingsService.getCurrentReadings(weatherStationId, 'humidity'),
        ReadingsService.getCurrentReadings(weatherStationId, 'gas_level')
      ])

      const [tempHistory, humidityHistory, gasHistory] = await Promise.all([
        ReadingsService.getHistoricalReadings(weatherStationId, 'temperature', 4*24*60),
        ReadingsService.getHistoricalReadings(weatherStationId, 'humidity', 4*24*60),
        ReadingsService.getHistoricalReadings(weatherStationId, 'gas_level', 4*24*60)
      ])

      // Process historical data
      const history = tempHistory.map((temp, index) => ({
        timestamp: temp.read_at,
        temperature: temp.value,
        humidity: humidityHistory[index]?.value || 0,
        toxicGases: gasHistory[index]?.value || 0
      }))

      // Calculate stats
      const calculateStats = (data: DataReading[]) => {
        const values = data.map(reading => reading.value)
        return {
          avg: values.reduce((sum, val) => sum + val, 0) / values.length || 0,
          max: Math.max(...values, 0),
          min: Math.min(...values, 0)
        }
      }

      return {
        temperature: {
          current: tempData[0],
          stats: calculateStats(tempHistory)
        },
        humidity: {
          current: humidityData[0],
          stats: calculateStats(humidityHistory)
        },
        toxicGases: {
          current: gasesData[0],
          stats: calculateStats(gasHistory)
        },
        history
      }
    },
    refetchInterval,
    refetchIntervalInBackground: true,
    staleTime: refetchInterval,
  })
} 