import {
  Badge,
  Container,
  Heading,
  Radio,
  RadioGroup,
  Stack,
  useColorMode,
} from "@chakra-ui/react";

const Appearance = () => {
  const { colorMode, toggleColorMode } = useColorMode();

  return (
    <>
      <Container maxW="full">
        <Heading size="sm" py={4}>
          Aparência
        </Heading>
        <RadioGroup onChange={toggleColorMode} value={colorMode}>
          <Stack>
            <Radio value="dark" colorScheme="teal">
              Dark Mode
              <Badge ml="1" colorScheme="teal">
                PADRÃO
              </Badge>
            </Radio>
            <Radio value="light" colorScheme="teal">
              Light Mode
            </Radio>
          </Stack>
        </RadioGroup>
      </Container>
    </>
  );
};
export default Appearance;
