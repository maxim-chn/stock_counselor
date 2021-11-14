import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Copyright } from 'src/app/copyright';

@Injectable({
  providedIn: 'root'
})
export class CopyrightService {

  public className: string;
  private copyrights: Array<Copyright>;

  constructor() {
    this.className = CopyrightService.name;
    this.copyrights = [
      new Copyright()
    ];
  }

  public getCopyrights(): Observable<Array<Copyright>> {
    return of(this.copyrights);
  }
}