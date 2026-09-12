export const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";
export async function request<T>(path:string, init?:RequestInit):Promise<T>{
  const response=await fetch(`${API}${path}`,{...init,headers:{"Content-Type":"application/json",...init?.headers},cache:"no-store"});
  if(!response.ok){const body=await response.json().catch(()=>({detail:"Request failed"}));throw new Error(body.detail??"Request failed")}
  return response.json() as Promise<T>;
}
export type Project={id:string;name:string;mode:string;objective:string;status:string;created_at:string};
export type Workflow={current_stage:string;state:string;blocked_reason:string|null};
export type Evidence={id:string;summary:string;source_ref:string;captured_at:string;confidence:number;freshness:string;estimated:boolean;pinned:boolean;rejected:boolean};
