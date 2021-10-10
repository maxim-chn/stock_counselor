import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Logo } from './logo';

@Injectable({
  providedIn: 'root'
})
export class LogoService {

  private logo: Logo;

  constructor() {
    /**
     * @TODO replace logo image with proper base64 png encoding.
    */
    this.logo = Logo.withAllAttributes("Stock Counselor Logo", "data:image/png;base64,BROKEN_VALUE");
  }

  public getLogo(): Observable<Logo> {
    return of<Logo>(this.logo);
  }
}
