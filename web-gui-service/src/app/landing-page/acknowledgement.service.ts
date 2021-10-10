import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Acknowledgement } from './acknowledgement';

@Injectable({
  providedIn: 'root'
})
export class AcknowledgementService {

  private acknowledgement: Acknowledgement

  constructor() {
    this.acknowledgement = Acknowledgement.withAllAttributes(
      [
        "There are links to external websites below.",
        "They all lead to the origins of different content used throughout the website development and deployment.",
        "Special thanks go to all those people who offer their content for free."
      ],
      "Special thanks"
    )
  }

  public getAcknowledgement(): Observable<Acknowledgement> {
    return of(this.acknowledgement);
  }
}
