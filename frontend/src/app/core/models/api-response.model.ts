export type ApiErrorValue = string | readonly string[];

export interface ApiErrorMap {
  readonly [key: string]: ApiErrorValue;
}

export interface ApiResponse<T> {
  readonly data: T;
  readonly message?: string;
  readonly errors?: ApiErrorMap;
}
