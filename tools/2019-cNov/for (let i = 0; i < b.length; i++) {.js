for (let i = 0; i < b.length; i++) {
  if (
    b
      .eq(i)
      .find('.external-html')
      .find('p')
      .text()
  ) {
    e = b
      .eq(i)
      .find('.external-html')
      .find('p')
      .text()
    f = e.split(':')
    c[f[0]] = f[1]
  }
}
