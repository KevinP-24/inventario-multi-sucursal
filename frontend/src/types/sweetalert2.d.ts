declare module 'sweetalert2' {
  export type SweetAlertIcon =
    | 'success'
    | 'error'
    | 'warning'
    | 'info'
    | 'question';

  export interface SweetAlertOptions {
    icon?: SweetAlertIcon;
    title?: string;
    text?: string;
    html?: string;
    toast?: boolean;
    position?: string;
    showConfirmButton?: boolean;
    showCancelButton?: boolean;
    confirmButtonText?: string;
    cancelButtonText?: string;
    reverseButtons?: boolean;
    focusCancel?: boolean;
    timer?: number;
    timerProgressBar?: boolean;
    buttonsStyling?: boolean;
    heightAuto?: boolean;
    target?: HTMLElement | null;
    customClass?: Record<string, string>;
    didOpen?: (element: HTMLElement) => void;
  }

  export interface SweetAlertResult<T = unknown> {
    isConfirmed: boolean;
    isDenied?: boolean;
    isDismissed?: boolean;
    value?: T;
    dismiss?: unknown;
  }

  export interface SweetAlertInstance {
    fire<T = unknown>(options: SweetAlertOptions): Promise<SweetAlertResult<T>>;
  }

  export interface SweetAlertStatic extends SweetAlertInstance {
    mixin(options: SweetAlertOptions): SweetAlertInstance;
    stopTimer(): void;
    resumeTimer(): void;
  }

  const Swal: SweetAlertStatic;
  export default Swal;
}
