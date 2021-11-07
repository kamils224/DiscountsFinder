import axiosInstance from "../axios-config/axios.instance";

export class ProductsTasksDto {
    constructor(public id: number,
                public created: string,
                public status: string,
                public pageUrl: string,
                public count: number) {
    }

    static fromJson(json: Record<string, any>) {
        const created = new Date(json.timestamp * 1000);
        return new ProductsTasksDto(json._id, `${created.toLocaleDateString()} ${created.toLocaleTimeString()}`,
            json.status, json.page_url, json.count);
    }
}

export default class ProductsTasksApi {

    baseUrl = "/api/discounts-finder/single-url-result";

    async getProductsTasks(): Promise<Array<ProductsTasksDto>> {
        const response = await axiosInstance.get(this.baseUrl);
        return response.data.map((item: Record<string, any>) => ProductsTasksDto.fromJson(item));
    }
}