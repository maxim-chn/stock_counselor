import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Copyright } from "../copyright";

@Injectable({
  providedIn: 'root'
})
export class CopyrightService {

  private copyrights: Array<Copyright>;

  constructor() {
    this.copyrights = [
      Copyright.withAllAttributes("Angular Framework", "https://angular.io/")
    ];
  }

  public getCopyrights(): Observable<Array<Copyright>> {
    return of(this.copyrights);
  }
}
