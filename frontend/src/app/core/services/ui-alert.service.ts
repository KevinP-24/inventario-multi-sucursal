import { inject, Injectable } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import Swal, {
  SweetAlertIcon,
  SweetAlertOptions,
  SweetAlertResult
} from 'sweetalert2';

export interface UiConfirmOptions {
  readonly title: string;
  readonly text?: string;
  readonly icon?: SweetAlertIcon;
  readonly confirmButtonText?: string;
  readonly cancelButtonText?: string;
  readonly reverseButtons?: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class UiAlertService {
  private readonly document = inject(DOCUMENT);

  private readonly modal = Swal.mixin({
    buttonsStyling: false,
    customClass: {
      popup: 'ms-alert-popup',
      title: 'ms-alert-title',
      htmlContainer: 'ms-alert-text',
      confirmButton: 'ms-alert-button ms-alert-button--primary',
      cancelButton: 'ms-alert-button ms-alert-button--ghost'
    },
    heightAuto: false
  });

  private readonly toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 2800,
    timerProgressBar: true,
    buttonsStyling: false,
    customClass: {
      popup: 'ms-alert-toast',
      title: 'ms-alert-toast__title'
    },
    didOpen: (element: HTMLElement) => {
      element.addEventListener('mouseenter', Swal.stopTimer);
      element.addEventListener('mouseleave', Swal.resumeTimer);
    }
  });

  success(message: string, title = 'Operacion completada'): Promise<SweetAlertResult<unknown>> {
    return this.modal.fire({
      icon: 'success',
      title,
      text: message
    });
  }

  error(message: string, title = 'No se pudo completar'): Promise<SweetAlertResult<unknown>> {
    return this.modal.fire({
      icon: 'error',
      title,
      text: message
    });
  }

  info(message: string, title = 'Informacion'): Promise<SweetAlertResult<unknown>> {
    return this.modal.fire({
      icon: 'info',
      title,
      text: message
    });
  }

  warning(message: string, title = 'Atencion'): Promise<SweetAlertResult<unknown>> {
    return this.modal.fire({
      icon: 'warning',
      title,
      text: message
    });
  }

  successToast(message: string, title = 'Listo'): Promise<SweetAlertResult<unknown>> {
    return this.toast.fire({
      icon: 'success',
      title,
      text: message
    });
  }

  errorToast(message: string, title = 'Error'): Promise<SweetAlertResult<unknown>> {
    return this.toast.fire({
      icon: 'error',
      title,
      text: message
    });
  }

  async confirm(options: UiConfirmOptions): Promise<boolean> {
    const result = await this.modal.fire({
      icon: options.icon ?? 'question',
      title: options.title,
      text: options.text,
      showCancelButton: true,
      focusCancel: true,
      reverseButtons: options.reverseButtons ?? true,
      confirmButtonText: options.confirmButtonText ?? 'Confirmar',
      cancelButtonText: options.cancelButtonText ?? 'Cancelar',
      target: this.document.body
    });

    return result.isConfirmed;
  }

  async fire(options: SweetAlertOptions): Promise<SweetAlertResult<unknown>> {
    return this.modal.fire(options);
  }
}
