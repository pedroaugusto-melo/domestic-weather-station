import type { CancelablePromise } from "./core/CancelablePromise"
import { OpenAPI } from "./core/OpenAPI"
import { request as __request } from "./core/request"

import type {
  Body_login_login_access_token,
  Message,
  NewPassword,
  Token,
  UserPublic,
  UpdatePassword,
  UserCreate,
  UserRegister,
  UsersPublic,
  UserUpdate,
  UserUpdateMe,
  ItemCreate,
  ItemPublic,
  ItemsPublic,
  ItemUpdate,
} from "./models"

import type { AnalysisResponse } from "../types/analysis"

export type TDataLoginAccessToken = {
  formData: Body_login_login_access_token
}
export type TDataRecoverPassword = {
  email: string
}
export type TDataResetPassword = {
  requestBody: NewPassword
}
export type TDataRecoverPasswordHtmlContent = {
  email: string
}

export class LoginService {
  /**
   * Login Access Token
   * OAuth2 compatible token login, get an access token for future requests
   * @returns Token Successful Response
   * @throws ApiError
   */
  public static loginAccessToken(
    data: TDataLoginAccessToken,
  ): CancelablePromise<Token> {
    const { formData } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/login/access-token",
      formData: formData,
      mediaType: "application/x-www-form-urlencoded",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Test Token
   * Test access token
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static testToken(): CancelablePromise<UserPublic> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/login/test-token",
    })
  }

  /**
   * Recover Password
   * Password Recovery
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static recoverPassword(
    data: TDataRecoverPassword,
  ): CancelablePromise<Message> {
    const { email } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/password-recovery/{email}",
      path: {
        email,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Reset Password
   * Reset password
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static resetPassword(
    data: TDataResetPassword,
  ): CancelablePromise<Message> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/reset-password/",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Recover Password Html Content
   * HTML Content for Password Recovery
   * @returns string Successful Response
   * @throws ApiError
   */
  public static recoverPasswordHtmlContent(
    data: TDataRecoverPasswordHtmlContent,
  ): CancelablePromise<string> {
    const { email } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/password-recovery-html-content/{email}",
      path: {
        email,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }
}

export type TDataReadUsers = {
  limit?: number
  skip?: number
}
export type TDataCreateUser = {
  requestBody: UserCreate
}
export type TDataUpdateUserMe = {
  requestBody: UserUpdateMe
}
export type TDataUpdatePasswordMe = {
  requestBody: UpdatePassword
}
export type TDataRegisterUser = {
  requestBody: UserRegister
}
export type TDataReadUserById = {
  userId: string
}
export type TDataUpdateUser = {
  requestBody: UserUpdate
  userId: string
}
export type TDataDeleteUser = {
  userId: string
}

export class UsersService {
  /**
   * Read Users
   * Retrieve users.
   * @returns UsersPublic Successful Response
   * @throws ApiError
   */
  public static readUsers(
    data: TDataReadUsers = {},
  ): CancelablePromise<UsersPublic> {
    const { limit = 100, skip = 0 } = data
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/users/",
      query: {
        skip,
        limit,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Create User
   * Create new user.
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static createUser(
    data: TDataCreateUser,
  ): CancelablePromise<UserPublic> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/users/",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Read User Me
   * Get current user.
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static readUserMe(): CancelablePromise<UserPublic> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/users/me",
    })
  }

  /**
   * Delete User Me
   * Delete own user.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static deleteUserMe(): CancelablePromise<Message> {
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/v1/users/me",
    })
  }

  /**
   * Update User Me
   * Update own user.
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static updateUserMe(
    data: TDataUpdateUserMe,
  ): CancelablePromise<UserPublic> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: "PATCH",
      url: "/api/v1/users/me",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Update Password Me
   * Update own password.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static updatePasswordMe(
    data: TDataUpdatePasswordMe,
  ): CancelablePromise<Message> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: "PATCH",
      url: "/api/v1/users/me/password",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Register User
   * Create new user without the need to be logged in.
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static registerUser(
    data: TDataRegisterUser,
  ): CancelablePromise<UserPublic> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/users/signup",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Read User By Id
   * Get a specific user by id.
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static readUserById(
    data: TDataReadUserById,
  ): CancelablePromise<UserPublic> {
    const { userId } = data
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/users/{user_id}",
      path: {
        user_id: userId,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Update User
   * Update a user.
   * @returns UserPublic Successful Response
   * @throws ApiError
   */
  public static updateUser(
    data: TDataUpdateUser,
  ): CancelablePromise<UserPublic> {
    const { requestBody, userId } = data
    return __request(OpenAPI, {
      method: "PATCH",
      url: "/api/v1/users/{user_id}",
      path: {
        user_id: userId,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Delete User
   * Delete a user.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static deleteUser(data: TDataDeleteUser): CancelablePromise<Message> {
    const { userId } = data
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/v1/users/{user_id}",
      path: {
        user_id: userId,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }
}

export type TDataTestEmail = {
  emailTo: string
}

export class UtilsService {
  /**
   * Test Email
   * Test emails.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static testEmail(data: TDataTestEmail): CancelablePromise<Message> {
    const { emailTo } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/utils/test-email/",
      query: {
        email_to: emailTo,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Health Check
   * @returns boolean Successful Response
   * @throws ApiError
   */
  public static healthCheck(): CancelablePromise<boolean> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/utils/health-check/",
    })
  }
}

export type TDataReadItems = {
  limit?: number
  skip?: number
}
export type TDataCreateItem = {
  requestBody: ItemCreate
}
export type TDataReadItem = {
  id: string
}
export type TDataUpdateItem = {
  id: string
  requestBody: ItemUpdate
}
export type TDataDeleteItem = {
  id: string
}

export class ItemsService {
  /**
   * Read Items
   * Retrieve items.
   * @returns ItemsPublic Successful Response
   * @throws ApiError
   */
  public static readItems(
    data: TDataReadItems = {},
  ): CancelablePromise<ItemsPublic> {
    const { limit = 100, skip = 0 } = data
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/items/",
      query: {
        skip,
        limit,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Create Item
   * Create new item.
   * @returns ItemPublic Successful Response
   * @throws ApiError
   */
  public static createItem(
    data: TDataCreateItem,
  ): CancelablePromise<ItemPublic> {
    const { requestBody } = data
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/items/",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Read Item
   * Get item by ID.
   * @returns ItemPublic Successful Response
   * @throws ApiError
   */
  public static readItem(data: TDataReadItem): CancelablePromise<ItemPublic> {
    const { id } = data
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/items/{id}",
      path: {
        id,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Update Item
   * Update an item.
   * @returns ItemPublic Successful Response
   * @throws ApiError
   */
  public static updateItem(
    data: TDataUpdateItem,
  ): CancelablePromise<ItemPublic> {
    const { id, requestBody } = data
    return __request(OpenAPI, {
      method: "PUT",
      url: "/api/v1/items/{id}",
      path: {
        id,
      },
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Delete Item
   * Delete an item.
   * @returns Message Successful Response
   * @throws ApiError
   */
  public static deleteItem(data: TDataDeleteItem): CancelablePromise<Message> {
    const { id } = data
    return __request(OpenAPI, {
      method: "DELETE",
      url: "/api/v1/items/{id}",
      path: {
        id,
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }
}

export type ChatMessage = {
  message: string
  sensorData: {
    temperature: number
    humidity: number
    toxicGases: number
  }
}

export type ChatResponse = {
  message: string
}

export class ChatService {
  /**
   * Send Chat Message
   * Send a message to the AI assistant with sensor data context
   * @returns ChatResponse Successful Response
   * @throws ApiError
   */
  public static sendMessage(data: ChatMessage): CancelablePromise<ChatResponse> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/v1/chat",
      body: data,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    })
  }
}

export class AnalysisService {
  public static async getAnalysis(temperature: number, humidity: number, toxicGases: number): CancelablePromise<AnalysisResponse> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/api/v1/analysis/suggestions',
      query: {
        temperature,
        humidity,
        toxic_gases: toxicGases
      },
    });
  }
}

export type DataReading = {
  id: string
  weather_station_id: string
  value: number
  read_at: string
}

export type ReadingType = 'temperature' | 'humidity' | 'gas_level'

export type WeatherStation = {
  id: string
  user_id: string
  weather_station_model_id: string
  name: string
  description: string | null
  part_number: string
}

export class ReadingsService {
  /**
   * Get Current Readings
   * Get the latest readings for a weather station
   * @returns DataReading[] Successful Response
   * @throws ApiError
   */
  public static getCurrentReadings(
    weatherStationId: string,
    type: ReadingType,
    limit: number = 1
  ): CancelablePromise<DataReading[]> {
    return __request(OpenAPI, {
      method: "GET",
      url: `/api/v1/data-readings/weather-stations/${weatherStationId}`,
      query: {
        type,
        limit,
        order: 'desc',
        order_by: 'read_at'
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Get Historical Readings
   * Get historical readings for a weather station
   * @returns DataReading[] Successful Response
   * @throws ApiError
   */
  public static getHistoricalReadings(
    weatherStationId: string,
    type: ReadingType,
    minutes: number = 60,
    skip: number = 0,
    limit: number = 1000000
  ): CancelablePromise<DataReading[]> {
    return __request(OpenAPI, {
      method: "GET",
      url: `/api/v1/data-readings/weather-stations/${weatherStationId}`,
      query: {
        type,
        minutes,
        skip,
        limit,
        order: 'asc',
        order_by: 'read_at'
      },
      errors: {
        422: `Validation Error`,
      },
    })
  }

  /**
   * Get Weather Stations
   * Get list of weather stations for the current user
   * @returns WeatherStation[] Successful Response
   * @throws ApiError
   */
  public static getWeatherStations(): CancelablePromise<WeatherStation[]> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/v1/weather-stations",
      errors: {
        422: `Validation Error`,
        403: `Not enough permissions`,
      },
    })
  }
}