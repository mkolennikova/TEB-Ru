#!/bin/bash

# Полный скрипт для преобразования Makefile под сборку в папку obj
# Работает в Google Colab / Linux

set -e  # останавливаться при ошибке

MAKEFILE="Makefile"
BACKUP="${MAKEFILE}.bak"
OBJDIR="obj"

echo "=== Преобразование Makefile для сборки в папку $OBJDIR ==="

# 1. Резервная копия
if [ -f "$MAKEFILE" ]; then
    cp "$MAKEFILE" "$BACKUP"
    echo "Создана резервная копия: $BACKUP"
else
    echo "Ошибка: файл $MAKEFILE не найден!"
    exit 1
fi

# 2. Удаляем все строки, начинающиеся с $(FC) (команды компиляции)
sed -i '/^$(FC)/d' "$MAKEFILE"
echo "Удалены старые команды компиляции."

# 3. Добавляем переменную OBJDIR и создание папки после include
sed -i "/^include gfortran_args/a OBJDIR = $OBJDIR\n\$(shell mkdir -p \$(OBJDIR))" "$MAKEFILE"
echo "Добавлены OBJDIR и mkdir."

# 4. Переопределяем OBJ с префиксом $(OBJDIR)/
# Сначала находим строку "OBJ = ..." и заменяем на "OBJ = $(addprefix $(OBJDIR)/, ...)"
# Но нужно учесть, что строка может быть разбита на несколько? В вашем Makefile она одна.
sed -i 's/^OBJ = /OBJ = \$(addprefix \$(OBJDIR)\/, /' "$MAKEFILE"
# Теперь нужно закрыть скобку в конце строки OBJ (она заканчивается на .o)
# Добавляем ')' после последнего .o
sed -i '/^OBJ = \$(addprefix .*/ s/$/)/' "$MAKEFILE"
echo "Обновлён список OBJ с путём к $OBJDIR."

# 5. Добавляем в конец Makefile общие правила и vpath
# Используем printf, чтобы корректно вставить табуляцию перед командами
cat >> "$MAKEFILE" << 'EOF'

# ----- Автоматические правила для сборки в obj/ -----
vpath %.F90 src_driver src_teb src_struct src_proxi_SVAT src_solar
vpath %.f90 src_driver src_teb src_struct src_proxi_SVAT src_solar
vpath %.F   src_teb
vpath %.f   src_teb

$(OBJDIR)/%.o: %.F90 | $(OBJDIR)
	$(FC) $(CPPDEFS) $(CPPFLAGS) $(FFLAGS) $(OTHERFLAGS) -c $< -o $@

$(OBJDIR)/%.o: %.f90 | $(OBJDIR)
	$(FC) $(CPPDEFS) $(CPPFLAGS) $(FFLAGS) $(OTHERFLAGS) -c $< -o $@

$(OBJDIR)/%.o: %.F | $(OBJDIR)
	$(FC) $(CPPDEFS) $(CPPFLAGS) $(FFLAGS) $(OTHERFLAGS) -c $< -o $@

$(OBJDIR)/%.o: %.f | $(OBJDIR)
	$(FC) $(CPPDEFS) $(CPPFLAGS) $(FFLAGS) $(OTHERFLAGS) -c $< -o $@
EOF

# Теперь исправляем правило driver1.exe и clean
sed -i '/^driver1.exe:/c driver1.exe: $(OBJ) | $(OBJDIR)' "$MAKEFILE"
# Заменяем строку с $(LD) на правильную с табуляцией
sed -i '/^driver1.exe:.*/a \\t$(LD) $(OBJ) -o driver1.exe $(LDFLAGS)' "$MAKEFILE"

# Обновляем clean: добавляем удаление папки obj и старых .mod
sed -i '/^clean:/a \\t-rm -rf $(OBJDIR)' "$MAKEFILE"

echo "Добавлены общие правила компиляции, исправлены driver1.exe и clean."

# 6. Добавляем флаги для модулей в gfortran_args (или в Makefile)
# Проверяем, есть ли уже флаг -J или -module
if grep -q "\-J\$(OBJDIR)" gfortran_args; then
    echo "Флаг -J уже присутствует в gfortran_args."
else
    # Добавляем после строки с FFLAGS для gfortran
    sed -i '/^FFLAGS = .*gfortran/s/$/ -J$(OBJDIR)/' gfortran_args
    echo "Добавлен флаг -J$(OBJDIR) в gfortran_args для gfortran."
fi

# Для ifort добавим -module, но только если не было
if grep -q "\-module \$(OBJDIR)" gfortran_args; then
    echo "Флаг -module уже присутствует в gfortran_args."
else
    sed -i '/^FFLAGS = .*ifort/s/$/ -module $(OBJDIR)/' gfortran_args
    echo "Добавлен флаг -module $(OBJDIR) в gfortran_args для ifort."
fi

# 7. Также можно добавить в сам Makefile условную установку флагов после include,
# чтобы быть уверенным, что они всегда есть.
# Но так как у вас отдельный файл gfortran_args, мы уже добавили туда.

echo "=== Преобразование завершено! ==="
echo "Запустите 'make clean && make' для сборки."
echo "Резервная копия: $BACKUP"