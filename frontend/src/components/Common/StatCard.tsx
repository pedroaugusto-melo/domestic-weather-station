import {
  Card,
  CardBody,
  Flex,
  Icon,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
} from "@chakra-ui/react"
import { IconType } from "react-icons"

interface Props {
  title: string
  value: string
  icon: IconType
  helpText: string
}

export function StatCard({ title, value, icon, helpText }: Props) {
  return (
    <Card>
      <CardBody>
        <Flex justify="space-between" align="center">
          <Stat>
            <StatLabel>{title}</StatLabel>
            <StatNumber>{value}</StatNumber>
            <StatHelpText>{helpText}</StatHelpText>
          </Stat>
          <Icon as={icon} boxSize={8} color="blue.500" />
        </Flex>
      </CardBody>
    </Card>
  )
} 