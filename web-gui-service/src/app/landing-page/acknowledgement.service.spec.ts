import { TestBed } from '@angular/core/testing';

import { AcknowledgementService } from './acknowledgement.service';

describe('AcknowledgementService', () => {
  let service: AcknowledgementService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AcknowledgementService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
