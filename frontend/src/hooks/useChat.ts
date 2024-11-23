import { useState } from "react"
import { ChatService } from "../client/services"
import type { ApiError } from "../client/core/ApiError"
import useCustomToast from "./useCustomToast"

interface SensorDataInput {
  temperature: number
  humidity: number
  toxicGases: number
}

export function useChat() {
  const [isLoading, setIsLoading] = useState(false)
  const showToast = useCustomToast()

  const sendMessage = async (message: string, sensorData: SensorDataInput) => {
    setIsLoading(true)
    try {
      const response = await ChatService.sendMessage({
        message,
        sensorData: {
          temperature: sensorData.temperature,
          humidity: sensorData.humidity,
          toxicGases: sensorData.toxicGases,
        },
      })
      return response.message
    } catch (error) {
      const apiError = error as ApiError
      showToast(
        "Error sending message",
        apiError.body?.detail || "Something went wrong",
        "error"
      )
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  return { sendMessage, isLoading }
} 