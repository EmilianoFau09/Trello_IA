import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {List} from '../models/list';
import {Card} from '../models/card';
import {Board} from '../models/board';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  constructor(private http: HttpClient) { }

  httpOptions = { headers: new HttpHeaders({ 'Content-Type': 'application/json' }) };
  baseUrl: string = 'http://127.0.0.1:8000';

  getBoardTitle(): Observable<any> {
    return this.http.get<any>(this.baseUrl + '/boardTitle', this.httpOptions);
  }

  getBoardTopic(): Observable<any> {
    return this.http.get<any>(this.baseUrl + '/boardTopic', this.httpOptions);
  }

  getTopics(): Observable<any> {
    return this.http.get<any>(this.baseUrl + '/topics', this.httpOptions);
  }

  putBoardTitle(boardTitle: string): Observable<any> {
    const requestBody = {
      boardTitle: boardTitle
    };
    return this.http.put<any>(this.baseUrl + '/boardTitle', requestBody, this.httpOptions);
  }

  putBoardTopic(boardTopic: string): Observable<any> {
    const requestBody = {
      boardTopic: boardTopic
    };
    return this.http.put<any>(this.baseUrl + '/boardTopic', requestBody, this.httpOptions);
  }

  getLists(): Observable<any> {
    return this.http.get<any>(this.baseUrl + '/list', this.httpOptions);
  }

  getCards(): Observable<any> {
    return this.http.get<any>(this.baseUrl + '/card/', this.httpOptions);
  }

  postList(title: string, description: string): Observable<any> {
    const requestBody: List = {
      title: title,
      description: description
    };
    return this.http.post<any>(this.baseUrl + '/list', requestBody, this.httpOptions);
  }

  postCard(description: string, idList: string, title: string): Observable<any> {
    const requestBody: Card = {
      description: description,
      idList: idList,
      title: title
    };
    console.log(requestBody)
    return this.http.post<any>(this.baseUrl + '/card', requestBody, this.httpOptions);
  }

  putList(idList: string, title: string, description: string): Observable<any> {
    const requestBody: List = {
      title: title,
      description: description
    };
    return this.http.put<any>(this.baseUrl + '/list/' + idList, requestBody, this.httpOptions);
  }

  putCard(description: string, idList: string, title: string, idCard: string): Observable<any> {
    const requestBody: Card = {
      description: description,
      idList: idList,
      title: title
    };
    return this.http.put<any>(this.baseUrl + '/card/' + idCard, requestBody, this.httpOptions);
  }

  deleteList(idList: string): Observable<any> {
    return this.http.delete<any>(this.baseUrl + '/list/' + idList, this.httpOptions);
  }

  deleteCard(idCard: string): Observable<any> {
    return this.http.delete<any>(this.baseUrl + '/card/' + idCard, this.httpOptions);
  }

  summarizeContent(text: string): Observable<any> {
    const requestBody: any = {
      text: text
    };
    return this.http.post<any>(this.baseUrl + '/ia/summarizeContent', requestBody, this.httpOptions);
  }

  expandContent(text: string): Observable<any> {
    const requestBody: any = {
      text: text
    };
    return this.http.post<any>(this.baseUrl + '/ia/expandContent', requestBody, this.httpOptions);
  }

  rewriteAndCorrectContent(text: string): Observable<any> {
    const requestBody: any = {
      text: text
    };
    return this.http.post<any>(this.baseUrl + '/ia/rewriteAndCorrectContent', requestBody, this.httpOptions);
  }

  generateVariations(text: string): Observable<any> {
    const requestBody: any = {
      text: text
    };
    return this.http.post<any>(this.baseUrl + '/ia/generateVariations', requestBody, this.httpOptions);
  }

  correctContent(text: string): Observable<any> {
    const requestBody: any = {
      text: text
    };
    return this.http.post<any>(this.baseUrl + '/ia/correctContent', requestBody, this.httpOptions);
  }

  generateListsForBoard(): Observable<any> {
    return this.http.post<any>(this.baseUrl + '/ia/generateListsForBoard', this.httpOptions);
  }

  generateCardsForList(text: string): Observable<any> {
    const requestBody: any = {
      text: text
    };
    return this.http.post<any>(this.baseUrl + '/ia/generateCardsForList', requestBody, this.httpOptions);
  }

  generateListDescription(text: string): Observable<any> {
    const requestBody: any = {
      text: text
    };
    return this.http.post<any>(this.baseUrl + '/ia/generateListDescription', requestBody, this.httpOptions);
  }

  generateCardDescription(text: string): Observable<any> {
    const requestBody: any = {
      text: text
    };
    return this.http.post<any>(this.baseUrl + '/ia/generateCardDescription', requestBody, this.httpOptions);
  }
}
