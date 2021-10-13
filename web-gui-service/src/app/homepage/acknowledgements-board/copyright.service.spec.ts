import { TestBed } from '@angular/core/testing';

import { CopyrightService } from './copyright.service';

describe('CopyrightService', () => {
  let service: CopyrightService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CopyrightService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
