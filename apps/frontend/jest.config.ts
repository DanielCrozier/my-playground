import type { Config } from "jest";

const config: Config = {
  preset: "ts-jest",
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["<rootDir>/src/__tests__/setupTests.ts"],
  moduleNameMapper: {
    // stub CSS / asset imports so Jest doesn't choke on them
    "\\.(css|less|scss|svg|png|jpg|gif|webp)$": "<rootDir>/src/__tests__/__mocks__/fileMock.ts",
  },
  transform: {
    "^.+\\.tsx?$": [
      "ts-jest",
      {
        tsconfig: "tsconfig.jest.json",
      },
    ],
  },
  testMatch: ["<rootDir>/src/**/*.test.{ts,tsx}"],
  collectCoverageFrom: ["src/**/*.{ts,tsx}", "!src/main.tsx", "!src/**/*.d.ts"],
};

export default config;
