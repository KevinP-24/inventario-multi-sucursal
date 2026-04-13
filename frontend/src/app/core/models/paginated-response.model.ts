import { ApiResponse } from './api-response.model';

export interface PaginationMeta {
  readonly page: number;
  readonly per_page: number;
  readonly total: number;
  readonly total_pages: number;
}

export interface PaginatedResponse<T> extends ApiResponse<readonly T[]> {
  readonly pagination: PaginationMeta;
}
