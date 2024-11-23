import { Select } from "@chakra-ui/react"

interface TimeRangeSelectorProps {
  value: number
  onChange: (value: number) => void
}

export function TimeRangeSelector({ value, onChange }: TimeRangeSelectorProps) {
  const timeRanges = [
    { label: "Últimos 5 minutos", value: 5 },
    { label: "Últimos 30 minutos", value: 30 },
    { label: "Última 1 hora", value: 60 },
    { label: "Últimas 6 horas", value: 6 * 60 },
    { label: "Últimas 12 horas", value: 12 * 60 },
    { label: "Últimas 24 horas", value: 24 * 60 },
    { label: "Últimos 3 dias", value: 3 * 24 * 60 },
    { label: "Últimos 7 dias", value: 7 * 24 * 60 },
  ]

  return (
    <Select
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
      maxW="200px"
    >
      {timeRanges.map((range) => (
        <option key={range.value} value={range.value}>
          {range.label}
        </option>
      ))}
    </Select>
  )
} 