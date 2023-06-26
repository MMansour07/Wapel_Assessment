using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Data.Entity;
using System.Threading.Tasks;

namespace EMS.Core.Dtos.General
{
    public class TableModel<T>
    {
        public Meta meta { get; set; }
        public PagedList<T> data { get; set; }
    }
    public class Meta
    {
        public int page { get; set; }
        public int pages { get; set; }
        public int perpage { get; set; }
        public int total { get; set; }
        public int totalFiltered { get; set; }
    }
    public class PagedList<T> : List<T>
    {
        [JsonConstructor]
        public PagedList() { }
        public int CurrentPage { get; set; }
        public int TotalPages { get; set; }
        public int PageSize { get; set; }
        public int pgeSize { get; set; }
        public int TotalCount { get; set; }
        public int TotalFiltered { get; set; }

        public PagedList(List<T> items, int Count, int pagenNumber, int pageSize, int totalcount)
        {
            this.CurrentPage = pagenNumber;
            this.PageSize = pageSize;
            this.TotalFiltered = totalcount;
            this.TotalCount = totalcount;
            this.TotalPages = (int)Math.Ceiling(Count / (double)pageSize);
            this.AddRange(items);
        }
        public static async Task<PagedList<T>> Create(IQueryable<T> Source, int pageNumber, int pageSize, int totalcount)
        {
            var Count = await Source.CountAsync();
            var items = await Source.Skip((pageNumber - 1) * pageSize).Take(pageSize).ToListAsync();
            return new PagedList<T>(items, Count, pageNumber, pageSize, totalcount);
        }
    }
}
