export interface ResourceInfo {
  name: string;
  is_taken: boolean;
  taken_by: string | null;
  taken_at: string | null;
  metadata: Record<string, any>;
}

export interface ResourceStatus {
  is_taken: boolean;
  taken_by: string | null;
  taken_at: string | null;
}

export interface AllResourcesStatus {
  publishers: Record<string, ResourceStatus>;
  environments: Record<string, ResourceStatus>;
}

export interface ActionResponse {
  success: boolean;
  message: string;
  status: ResourceStatus;
  previous_owner?: string;
}
